# from ..database import db
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from src.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum

# Base Models

class Base:
    now = datetime.now()
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=now)
    modified_at = db.Column(db.DateTime, nullable=False, default=now, onupdate=now)

# Custom Models

class User(UserMixin, Base, db.Model):
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_loggedin_at = db.Column(db.DateTime, default=None)

class Topic(Base, db.Model):
    name = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(50), nullable=False)
    uuid = db.Column(db.String(36), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)

class Post(Base, db.Model):
    topic = db.Column(db.String(50), nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    content = db.Column(db.String(1024))

def init():
    db.create_all()