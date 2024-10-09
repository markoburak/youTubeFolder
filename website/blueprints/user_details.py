from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.models import User
from website import db
from flask_login import login_required, current_user

user_details = Blueprint('user_details', __name__)


@user_details.route("/user_details", methods=["GET", "POST"])
@login_required
def user_details_get():
    if request.method == "GET":
        return render_template("user_details.html", user=current_user)
    elif request.method == "POST":
        user_data = User.query.filter_by(id=current_user.id).first()
        if user_data:
            user_data.first_name = request.form["first_name"]
            user_data.last_name = request.form["last_name"]
            user_data.email = request.form["email"]
            if not request.form["first_name"]:
                flash('First name must be at least 1 character', category='error')
            elif not request.form["last_name"]:
                flash('Last name must be at least 1 character', category='error')
            elif len(request.form["email"]) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                try:
                    db.session.commit()
                    flash('Updated user data!', category='success')
                except:
                    flash('Something didn\'t work', category='error')
        else:
            flash('Cannot update the user!', category='error')
        return redirect(url_for('user_details_bp.user_details'))
