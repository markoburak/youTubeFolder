import datetime
import json
import urllib

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
            if "www.youtube.com" not in url:
                flash('Provided unsupported link!', category='error')
                return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))

            if "?v=" in url:
                youtube_id = url.split("?v=")[1].split("&")[0]
            else:
                flash('Provided unsupported link!', category='error')
                return redirect((url_for('links_view.youTubeLinks', category_id=category_id)))

            # get additional info, such as title
            params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % youtube_id}
            base_url = "https://www.youtube.com/oembed"
            query_string = urllib.parse.urlencode(params)
            base_url = base_url + "?" + query_string

            with urllib.request.urlopen(base_url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
                title = data['title']

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
    # Find the link by ID
    link_to_delete = YouTubeLink.query.filter_by(id=link_id).first()
    category_id = link_to_delete.category_id

    if link_to_delete:
        # Remove the category from the database
        db.session.delete(link_to_delete)
        db.session.commit()
        # flash('Link deleted!', category='success')
    else:
        flash('Link not found!', category='error')

    return redirect(url_for('links_view.youTubeLinks', category_id=category_id))


@links_view.route("/back_to_category", methods=["GET"])
@login_required
def back_to_category():
    return redirect(url_for('category_view.index'))
