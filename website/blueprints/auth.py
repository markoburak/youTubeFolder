import random, string
from flask import Blueprint, render_template, request, redirect, url_for, flash
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, Category
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for(('category_view.index')))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    def_email, def_first_name, def_last_name = "", "", ""
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 characters.', category='error')
        else:
            def_email = email
            def_first_name = first_name
            def_last_name = last_name
            if password1 != password2:
                flash('Password don\'t match', category='error')
            elif len(password1) < 8:
                flash('Password must be at least 7 characters', category='error')
            else:

                new_user = User(email=email, first_name=first_name, last_name=last_name,
                                password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember=True)
                user = User.query.filter_by(email=email).first()

                default_category = Category(name="default", user_id=user.id)
                db.session.add(default_category)
                db.session.commit()
                # flash('Account created!', category='success')
                return redirect(url_for('category_view.index'))

    return render_template("sign_up.html", user=current_user, def_email=def_email, def_first_name=def_first_name,
                           def_last_name=def_last_name)
