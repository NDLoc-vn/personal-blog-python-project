from . import db
from flask_login import UserMixin
from datetime import timezone
from sqlalchemy.sql import func
from sqlalchemy import Boolean

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    private = db.Column(Boolean)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    contentAndTag = db.relationship("ContentAndTag")

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_tag = db.Column(db.String(150), unique=True)
    contentAndTag = db.relationship("ContentAndTag")

class ContentAndTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey("content.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    def __init__(self, username, password):
        self.username = username
        self.password = password
