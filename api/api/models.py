from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    last = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(
        db.String(150), nullable=False, default="default.jpg")
    password = db.Column(db.String(256))
    admin = db.Column(db.Boolean, default=False)
    premium = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, name, last, username, image_file="default.jpg"):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.username = username
        self.name = name
        self.last = last
        self.image_file = image_file if image_file else "default.jpg"

    def change(self):
        self.premium = True if self.premium == False else False

    def promote(self):
        self.admin = True

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        username = kwargs.get('username')

        if not email or not password:
            if not username:
                return None

        user = cls.query.filter_by(email=email).first()
        if not user:
            user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email, username=self.username, name=self.name, last=self.last, admin=self.admin, premium=self.premium, image_file=self.image_file)


class Pdf(db.Model):
    __tablename__ = "pdf"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    data = db.Column(db.String(255))
    user_id = db.Column(db.Integer)

    def __init__(self, name, data, user_id):
        self.name = name
        self.data = data
        self.user_id = user_id

    def __repr__(self):
        return super().__repr__()

    def to_dict(self):

        return dict(id=self.id, name=self.name, data=self.data, user_id=self.user_id)


class PremiumUser(User):
    __tablename__ = 'premium'
    credit_card = db.Column(db.String(50))
