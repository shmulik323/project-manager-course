from functools import wraps
from datetime import datetime, timedelta
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, current_app, render_template, flash
from flask import send_file, Response
from flask_mail import Mail, Message
from.form import ContactForm
import jwt
import requests
from time import perf_counter
import os
import base64
import json


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


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    return requests.get('http://localhost:3000/{}'.format(path)).text

@app.route('api/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='the email from application', recipients=['mishel110393@gmail.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)

@app.route('api/reset',methods=['GET'])
@token_required
def reset_password():
    data = request.get_json()
    user=User.db.query.filter_by(email=data['email']).first()
    if user: 
        if check_password_hash(user.password,data['old']):
            password=generate_password_hash(data['new'], method='sha256')
            User=password
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
            return jsonify({'message': 'User does not exist'}), 401
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('api/cancel',methods=['GET', 'POST'])
@token_required
def cancel_premium(User):
    if User.premium:
        User.change()
    else:
        return jsonify({'message': 'User without premium status'}), 401
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api.route('api/new_admin', methods=('POST',))
@token_required
def new_manager(User):
    if User.admin:
        data = request.get_json()
        user = User(**data)
        user.promote()
    else:
        return jsonify({'message': 'User is not an admin'}), 401
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api.route('api/add_permissions', methods=('POST',))
@token_required
def add_permissions(User):
    if User.admin:
        data = request.get_json()
        user=User.db.filter_by(email=data['email']).first()
        if user:
            if data['premium']:
                user.change()
            if data['admin']:
                user.promote()
        else:
            return jsonify({'message': 'User does not exist'}), 401
    else:
        return jsonify({'message': 'User is not an admin'}), 401
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

##TO_DO
##finish authentication process
@api.route('api/edit_email', methods=('POST',))
@token_required
def edit_email(User):
    data = request.get_json()
    user = User.authenticate(**data)
    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401
    else:
        user.email=data['new email']
    db.session.commit()
    return jsonify(user.to_dict()), 201