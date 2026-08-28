import os
from urllib.parse import quote_plus

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config_file.config as config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    database_url = os.environ.get('DATABASE_URL')
    production_database_configured = all(
        (config.db_host, config.db_name, config.db_user, config.db_password)
    )

    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    elif production_database_configured:
        app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        SQLALCHEMY_DATABASE_URI = (
            "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"
            "?charset=utf8mb4"
        ).format(
            username=quote_plus(config.db_user),
            password=quote_plus(config.db_password),
            hostname=config.db_host,
            databasename=quote_plus(config.db_name),
        )
    else:
        db_host = config.db_host_local
        db_name = config.db_name_local
        db_user = config.db_user_local
        db_password = config.db_password_local
        SQLALCHEMY_DATABASE_URI = (
            "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}"
            "?charset=utf8mb4"
        ).format(
            username=quote_plus(db_user),
            password=quote_plus(db_password),
            hostname=db_host,
            databasename=quote_plus(db_name),
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from website.blueprints.category_view import category_view
    from website.blueprints.auth import auth
    from website.blueprints.links import links_view
    from website.blueprints.user_details import user_details

    app.register_blueprint(category_view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(links_view, url_prefix="/")
    app.register_blueprint(user_details, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = ''

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app
