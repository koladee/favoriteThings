from api import db, login_manager
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(100), index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password = db.Column(db.String(100), index=True, nullable=False)
    list = db.relationship('List', backref='user', lazy=True)
    cat = db.relationship('Category', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(name='{self.username}')>"


class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    list = db.relationship('List', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category(name='{self.name}' user='{self.user_id}')>"


class CategorySchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    user_id = fields.Integer()


class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    rid = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ranking = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cat = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False)
    modified_date = db.Column(db.TIMESTAMP, index=True)
    log = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Request(user='{self.user_id}', title='{self.title}', ranking='{self.ranking}')>"


class ListSchema(ma.Schema):
    id = fields.Integer()
    rid = fields.String()
    title = fields.String()
    description = fields.String()
    ranking = fields.Integer()
    user_id = fields.Integer()
    cat = fields.Integer()
    created_date = fields.Time()
    modified_date = fields.DateTime()
    log = fields.String()
