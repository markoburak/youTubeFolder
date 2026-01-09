from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    created_date = db.Column(db.Date(), default=func.now())
    category = db.relationship('Category')


class Category(db.Model):
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True)
    starred = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(50))
    emoji = db.Column(db.String(10), default="📁")
    created_date = db.Column(db.Date(), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    youtubelink = db.relationship('YouTubeLink')


# https://img.youtube.com/vi/".$video_id."/hqdefault.jpg

class YouTubeLink(db.Model):
    __tablename__ = "youTubeLink"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400))
    img_url = db.Column(db.String(400))
    title = db.Column(db.String(400))
    created_date = db.Column(db.Date(), default=func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))
