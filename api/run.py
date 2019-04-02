from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import requests
from flask_cors import CORS, cross_origin
import datetime
from flask_admin import Admin
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
CORS(app)
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    last = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(
        db.String(150), nullable=False, default="default.jpg")
    password = db.Column(db.String(80))
    premium = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean)

    def change(self):
        self.premium = True if self.premium == False else False 

class PremiumUser(User):
    credit_card = db.Column(db.String(50))


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return jsonify({'massege': 'Token is missing'}), 401


admin = Admin(app)
admin.add_view(MyModelView(User, db.session))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token - request.headers['x-access-token']
        if not token:
            return jsonify({'massege': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except expression as identifier:
            return jsonify({'massege': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/auth/users', methods=['GET'])
def get_all_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['last'] = user.last
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['premium'] =user.premium
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/api/auth/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'massege': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['last'] = user.last
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['premium'] =user.premium
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/api/auth/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = PremiumUser(public_id=str(uuid.uuid4()), name=data['name'], last=data['last'],
                    username=data['username'], email=data['email'], password=hashed_password, admin=False,credit_card=credit_card)
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})

@app.route('/api/auth/premium', methods=['POST'])
def create_premium():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = PremiumUser(public_id=str(uuid.uuid4()), name=data['name'], last=data['last'],
                    username=data['username'], email=data['email'], password=hashed_password, admin=False)
    new_user.change()
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New premium user created!'})

@app.route('/api/auth/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'massege': 'No user found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'user is an admin now!'})


@app.route('/api/auth/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'massege': 'No user found'})
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'user hes been deleted!'})


@app.route('/api/auth/login', methods=['GET', 'POST'])
@cross_origin()
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify1', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify2', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8'), 'username': user.username, 'name': user.name})

    return make_response('Could not verify3', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/api/auth/logout')
@cross_origin()
def logout():
    logout_user()
    return "logged out"


if __name__ == '__main__':
    app.run(debug=True)
