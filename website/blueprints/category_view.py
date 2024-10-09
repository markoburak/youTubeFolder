import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User, Category
from website import db
from sqlalchemy import or_
from flask_login import login_required, current_user
import re

category_view = Blueprint('category_view', __name__)


@category_view.route("/", methods=["GET"])
@login_required
def index():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.created_date)
    return render_template("main.html", user=current_user, categories=categories)


@category_view.route("/add_category", methods=["POST"])
@login_required
def add_category():
    if request.method == "POST":
        name = request.form.get('category_name')

        if name == "default":
            flash('Cannot add a default category!', category='error')
            return redirect(url_for('category_view.index'))

        if name:
            item = Category(name=name, user_id=current_user.id, created_date=datetime.date.today())
            db.session.add(item)
            db.session.commit()
            # flash('Category added!', category='success')
    return redirect(url_for('category_view.index'))


@category_view.route("/remove_category/<int:category_id>", methods=["POST"])
@login_required
def remove_category(category_id):
    # Find the category by ID and ensure it belongs to the current user
    category_to_delete = Category.query.filter_by(id=category_id, user_id=current_user.id).first()

    if category_to_delete.name == "default":
        flash('Cannot delete default category!', category='error')
        return redirect(url_for('category_view.index'))

    if category_to_delete:
        # Remove the category from the database
        db.session.delete(category_to_delete)
        db.session.commit()
        # flash('Category deleted!', category='success')
    else:
        flash('Category not found!', category='error')

    return redirect(url_for('category_view.index'))


@category_view.route("/update_category/<int:category_id>", methods=["POST"])
@login_required
def update_category(category_id):
    # Find the category by ID and ensure it belongs to the current user
    category_to_update = Category.query.filter_by(id=category_id, user_id=current_user.id).first()

    if category_to_update.name == "default":
        flash('Cannot update default category!', category='error')
        return redirect(url_for('category_view.index'))

    if category_to_update:
        name_to_update = request.form.get('category_update_name')
        # Remove the category from the database
        category_to_update.name = name_to_update
        db.session.commit()
        # flash('Category updated!', category='success')
    else:
        flash('Category not found!', category='error')

    return redirect(url_for('category_view.index'))