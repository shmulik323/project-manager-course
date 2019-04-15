from functools import wraps
from datetime import datetime, timedelta
from werkzeug import secure_filename
from flask import Blueprint, jsonify, request, current_app, render_template, Response
from flask import send_file, Response
import jwt
from flask_cors import cross_origin

import requests
from time import perf_counter
import os
import base64
import json
from flask_mail import Mail, Message

from .models import db, User

api = Blueprint('api', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            # 401 is Unauthorized HTTP status code
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@api.route('api/hello/<string:name>/')
def say_hello(name):
    response = {'msg': "Hello {}".format(name)}
    return jsonify(response)


@api.route('api/register', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/edit_user', methods=('POST',))
@token_required
def edit(User):
    request = json.loads(request.get_data())
    user = User.query.filter_by(username=request.username).first()
    user.username = request.username
    user.email = request.email
    user.image_file = request.image_file
    user.name = request.name
    user.last = request.last

    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/auth/login', methods=('OPTIONS', 'POST', 'GET'))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})


@api.route('api/auth/user', methods=('OPTIONS', 'POST', 'GET'))
@token_required
def return_user(User):

    return jsonify(user={'user': User.username, 'email': User.email, 'admin': User.admin, 'premium': User.premium, 'name': User.name, 'last': User.last, 'image_file': User.image_file})


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('api/uploader', methods=['POST'])
def upload_me():

    if request.method == 'POST':
        """ Receive base 64 encoded image """
        start = perf_counter()
        print('Request received')
        request_data = json.loads(request.get_data())
        data = request_data['data'][5:]

        with open('./uploads/'+request_data['name'], 'w') as wf:
            wf.write(data)

        print('Saved in file.')
        print('Time elapsed: {}'.format(perf_counter() - start))
        return Response(status=200)


@api.route('api/uploader', methods=['GET'])
@token_required
def get_image(User):
    if request.method == 'GET':
        path = './uploads/'+User.image_file
        """ Show saved image """
        if os.path.exists(path):
            with open(path, 'r') as rf:
                data = rf.read()
                mimetype, image_string = data.split(';base64,')
                image_bytes = image_string.encode('utf-8')
                return Response(base64.decodebytes(image_bytes), mimetype=mimetype)


@api.route("api/send_mail", methods=['POST'])
def send_mail():
    request_data = json.loads(request.get_data())
    mail = Mail(current_app)
    try:
        msg = Message(subject="message from" + request_data["name"],
                      sender=current_app.config.get("MAIL_USERNAME"),
                      # replace with your email for testing
                      recipients=[request_data["dev"]],
                      )
        msg.body = request_data["message"]
        print(current_app)
        mail.send(msg)

        return 'Mail sent!'
    except Exception as e:
        return(str(e))
    response = {'msg': "Hello"}
    return jsonify(response)


@api.route('/api/upload', methods=['GET', 'POST'])
@cross_origin(allow_headers=['Content-Type'])
def uploader_me():
    if request.method == 'GET':
        """ Show saved image """
        if os.path.exists('file.img'):
            with open('file.img', 'r') as rf:
                data = rf.read()
                mimetype, image_string = data.split(';base64,')
                image_bytes = image_string.encode('utf-8')
                return Response(base64.decodebytes(image_bytes), mimetype=mimetype)

    if request.method == 'POST':
        """ Receive base 64 encoded image """
        start = perf_counter()
        print('Request received')
        request_data = json.loads(request.get_data())
        data = request_data['data'][5:]

        with open('file.img', 'w') as wf:
            wf.write(data)

        print('Saved in file.')
        print('Time elapsed: {}'.format(perf_counter() - start))
        return Response(status=200)

    return render_template('index.html')


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    return requests.get('http://localhost:3000/{}'.format(path)).text