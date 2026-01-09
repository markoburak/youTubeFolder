from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config_file.config as config
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # local for testing purposes
    # using local default mysql connection with specified db(already created)
    local = False
    if local:
        db_host = config.db_host_local
        db_name = config.db_name_local
        db_user = config.db_user_local
        db_password = config.db_password_local
    # connect to hosting server db
    else:
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        db_host = config.db_host
        db_name = config.db_name
        db_user = config.db_user
        db_password = config.db_password

    # set DB_URI, connect to local DB or hosting DB
    if local:
        SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    else:
        SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}?charset=utf8mb4".format(
            username=db_user,
            password=db_password,
            hostname=db_host,
            databasename=db_name,
        )
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)

    from . import models

    from website.blueprints.category_view import category_view
    from website.blueprints.auth import auth
    from website.blueprints.links import links_view
    from website.blueprints.user_details import user_details

    app.register_blueprint(category_view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(links_view, url_prefix="/")
    app.register_blueprint(user_details, url_prefix="/")

    if local:
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = ''

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')
