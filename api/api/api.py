from .models import db, User
import json
import base64
import os
from time import perf_counter
import requests
from flask_cors import cross_origin
import jwt
from functools import wraps
from datetime import datetime, timedelta
from werkzeug import secure_filename
from flask import Blueprint, jsonify, request, current_app, render_template, Response, make_response, send_from_directory
from flask import send_file
from flask_mail import Mail, Message
from fpdf import FPDF, HTMLMixin

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
            print(data)
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


@api.route('api/edit_picture', methods=('POST',))
def edit_picture():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'])
    if user:
        user.image_file = data['image_file']
        db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/edit_user', methods=('POST',))
@token_required
def edit(User):
    request = json.loads(request.get_data())
    user = User.query.filter_by(username=request.username).first()
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
        dirName = './uploads/'+request_data['username']+'/Profile_Pic'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        with open(dirName+'/'+request_data['name'], 'w') as wf:
            wf.write(data)

        print('Saved in file.')
        print('Time elapsed: {}'.format(perf_counter() - start))
        return Response(status=200)


@api.route('api/uploader', methods=['GET'])
@token_required
def get_image(User):
    if request.method == 'GET':
        path = './uploads/'+User.username+'/Profile_Pic/'+User.image_file
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
        msg = Message("message from" + request_data["name"],
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


@api.route('api/pdf', methods=['GET', 'POST'])
@token_required
def render_pdf_weasyprint(User):
    request_data = json.loads(request.get_data())

    class MyFPDF(FPDF, HTMLMixin):
        pass

    pdf = MyFPDF()
    pdf.add_page()
    pdf.write_html(request_data["html"])
    response = make_response(pdf.output(
        'uploads/'+User.username + '/PDF_Files/' + request_data["name"]+'.pdf', 'F'))
    response.headers.set('Content-Disposition',
                         'attachment', filename=request_data["name"]+'.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    def download(filename):
        dirName = 'uploads/'+User.username+'/PDF_Files'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        uploads = os.path.join(current_app.root_path,
                               dirName)
        return send_from_directory(directory=uploads, filename=filename, mimetype='application/pdf')

    return download("html.pdf")


@api.route('api/reset', methods=['GET'])
@token_required
def reset_password():
    data = request.get_json()
    user = User.db.query.filter_by(email=data['email']).first()
    if user:
        if check_password_hash(user.password, data['old']):
            password = generate_password_hash(data['new'], method='sha256')
            user.password = password
        else:
            return jsonify({'message': 'Invalid password'}), 401
    else:
        return jsonify({'message': 'User does not exist'}), 401
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/cancel', methods=['GET', 'POST'])
@token_required
def cancel_premium(User):
    data = request.get_json()
    user = User.db.query.filter_by(email=data['email']).first()
    if user.premium:
        user.change()
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
        user = User.db.filter_by(email=data['email']).first()
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


@api.route('api/edit_email', methods=('POST',))
@token_required
def edit_email(User):
    data = request.get_json()
    user = User.query.filter_by(email=data['new'])
    if user:
        return jsonify({'message': 'Email already exists'}), 401
    else:
        user.User.query.filter_by(email=data['old'])
        user.email = data['new']
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/change_username', methods=('POST',))
@token_required
def change_username(User):
    data = request.get_json()
    user = User.query.filter_by(username=data['new'])
    if user:
        return jsonify({'message': 'Username already exists'}), 401
    else:
        user.User.query.filter_by(username=data['old'])
        user.username = data['new']
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def catch_all(path):
    return requests.get('http://localhost:3000/{}'.format(path)).text
