import datetime
import json
import urllib

import pytube.exceptions
from pytube import YouTube
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import Category, YouTubeLink
from website import db
from flask_login import login_required, current_user

links_view = Blueprint('links_view', __name__)


@links_view.route("/links/<int:category_id>", methods=["GET"])
@login_required
def youTubeLinks(category_id):
    category = Category.query.filter_by(user_id=current_user.id, id=category_id).first()
    if not category:
        flash('Broken category, please contact support!', category='error')
        return redirect(url_for('category_view.index'))

    youTubeLinksAll = YouTubeLink.query.filter_by(category_id=category_id).order_by(YouTubeLink.created_date)
    return render_template("youtubelink.html", user=current_user, category=category, links=youTubeLinksAll)


@links_view.route("/priority", methods=["GET"])
@login_required
def priority():
    priority_links = (
        db.session.query(YouTubeLink, Category)
        .join(Category, YouTubeLink.category_id == Category.id)
        .filter(Category.user_id == current_user.id, YouTubeLink.is_priority.is_(True))
        .order_by(YouTubeLink.created_date.desc(), YouTubeLink.id.desc())
        .all()
    )

    return render_template(
        "priority.html",
        user=current_user,
        priority_links=priority_links,
    )


@links_view.route("/add_link/<int:category_id>", methods=["POST"])
@login_required
def add_link(category_id):
    if request.method == "POST":
        url = request.form.get('url')

        if url:
            # final params
            youtube_id = ""
            title = ""
            processed_url = ""
            img_url = ""

            # add the link img testing
            if "youtube.com" not in url and "youtu.be" not in url:
                flash('Provided unsupported link!', category='error')
                return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))

            if "?v=" in url:
                youtube_id = url.split("?v=")[1].split("&")[0]
            elif "youtu.be" in url:
                youtube_id = url.split("youtu.be/")[1].split("?")[0]
            else:
                flash('Provided unsupported link!', category='error')
                return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))

            if len(youtube_id) != 11:
                flash('Provided unsupported link!', category='error')
                return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))

            # Ideal solution but for the paid pythonanywhere version
            # if "?v=" not in url:
            #     flash('Provided unsupported link!', category='error')
            #     return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))
            #
            # try:
            #     yt_play = YouTube(url)
            # except pytube.exceptions.RegexMatchError:
            #     flash('Provided unsupported link!', category='error')
            #     return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))
            #
            # if not yt_play.title or not yt_play.video_id:
            #     flash('Provided unsupported link!', category='error')
            #     return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))
            #
            # title = yt_play.title
            # youtube_id = yt_play.video_id

            processed_url = f"https://www.youtube.com/watch?v={youtube_id}"

            img_url = f"https://img.youtube.com/vi/{youtube_id}/hqdefault.jpg"
            new_link = YouTubeLink(url=processed_url, img_url=img_url, title=title, created_date=datetime.date.today(),
                                   category_id=category_id)
            db.session.add(new_link)
            db.session.commit()
            # flash('Link has added!', category='success')
    return redirect(url_for('links_view.youTubeLinks', category_id=category_id))


@links_view.route("/remove_link/<int:link_id>", methods=["POST"])
@login_required
def remove_link(link_id):
    link_to_delete = (
        YouTubeLink.query
        .join(Category, YouTubeLink.category_id == Category.id)
        .filter(YouTubeLink.id == link_id, Category.user_id == current_user.id)
        .first()
    )

    if not link_to_delete:
        flash('Link not found!', category='error')
        return redirect(url_for('category_view.index'))

    category_id = link_to_delete.category_id
    db.session.delete(link_to_delete)
    db.session.commit()

    if request.form.get('redirect_to') == 'priority':
        return redirect(url_for('links_view.priority'))

    return redirect(url_for('links_view.youTubeLinks', category_id=category_id))


@links_view.route("/back_to_category", methods=["GET"])
@login_required
def back_to_category():
    return redirect(url_for('category_view.index'))

@links_view.route("/update_link/<int:link_id>", methods=["POST"])
@login_required
def update_link(link_id):
    link_to_update = (
        YouTubeLink.query
        .join(Category, YouTubeLink.category_id == Category.id)
        .filter(YouTubeLink.id == link_id, Category.user_id == current_user.id)
        .first()
    )

    if not link_to_update:
        flash('Link not found!', category='error')
        return redirect(url_for('category_view.index'))

    link_to_update.title = request.form.get('link_update_name')
    link_to_update.is_priority = request.form.get('is_priority') == 'true'
    db.session.commit()

    if request.form.get('redirect_to') == 'priority':
        return redirect(url_for('links_view.priority'))

    return redirect(url_for('links_view.youTubeLinks', category_id=link_to_update.category_id))
