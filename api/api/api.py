from .models import db, User, Pdf
import json
from mimetypes import MimeTypes
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
from flask_login import login_user, logout_user
from flask_mail import Mail, Message
from fpdf import FPDF, HTMLMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
            print(token)
            data = jwt.decode(token, "ani")
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
    request_deta = request.get_json()
    user = User.query.filter_by(username=User.username).first()
    user.name = request_deta['name']
    user.last = request_deta['last']
    db.session.commit()
    return jsonify({"msg": "seccess"}), 201


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
    if user.admin:
        login_user(user)
    return jsonify({'token': token.decode('UTF-8')})


@api.route('api/auth/logout', methods=('POST', 'GET'))
@token_required
def say_hello(User):
    logout_user()
    response = {'msg': "Loged-Out :{}".format(User.username)}
    return jsonify(response)


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


@api.route('api/update-image', methods=['POST'])
@token_required
def update_image(User):

    if request.method == 'POST':

        """ Receive base 64 encoded image """
        start = perf_counter()
        print('Request received')
        request_data = json.loads(request.get_data())
        data = request_data['data'][5:]
        dirName = './uploads/'+User.username+'/Profile_Pic'
        if not os.path.exists(dirName):
            os.mkdir('./uploads/'+User.username)
            os.mkdir(dirName)
        with open(dirName+'/'+request_data['name'], 'w') as wf:
            wf.write(data)

        print('Saved in file.')
        print('Time elapsed: {}'.format(perf_counter() - start))
    User.image_file = request_data['name']
    db.session.commit()
    return Response(status=200)


@api.route('api/uploader', methods=['GET'])
@token_required
def get_image(User):
    if request.method == 'GET':
        if User.image_file == 'default.jpg':
            path = './uploads/default.jpg'
        else:
            path = './uploads/'+User.username+'/Profile_Pic/'+User.image_file
        """ Show saved image """
        if os.path.exists(path):
            with open(path, 'r') as rf:
                data = rf.read()
                mimetype, image_string = data.split(';base64,')
                image_bytes = image_string.encode('utf-8')
                return Response(base64.decodebytes(image_bytes), mimetype=mimetype)


@api.route('api/pdf', methods=['POST', "GET"])
@token_required
def render_pdf_weasyprint(User):
    if request.method == 'POST':
        request_data = json.loads(request.get_data())

        data = request.get_json()

        class MyFPDF(FPDF, HTMLMixin):
            pass

        pdf = MyFPDF()
        pdf.add_page()
        pdf.add_font(
            'DejaVu', '', './api/fonts/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('Arial', '', 14)
        pdf.write_html(request_data["data"])
        pdfData = Pdf(
            name=request_data["name"], data=request_data["data"], user_id=User.id)
        print(pdfData)
        db.session.add(pdfData)
        db.session.commit()
        dirName = 'uploads/'+User.username+'/PDF_Files'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        response = make_response(pdf.output(
            dirName+'/' + request_data["name"]+'.pdf', 'F'))
        response.headers.set('Content-Disposition',
                             'attachment', filename=request_data["name"]+'.pdf')
        response.headers.set('Content-Type', 'application/pdf')
        return jsonify({"msg": "saved"}), 201
    if request.method == 'GET':
        pdfDataArrey = Pdf.query.filter_by(user_id=User.id).all()
        newArrey = []
        for pdf in pdfDataArrey:
            temp = pdf.to_dict()
            newArrey.append({"name": temp["name"], "data": temp["data"]})
            print(pdf.__dict__)
        return jsonify(pdfs=newArrey)


@api.route('api/remove_pdf', methods=['POST', "GET"])
@token_required
def delete_pdf(User):
    data = request.get_json()
    if request.method == 'POST':
        pdfData = Pdf.query.filter_by(name=data["name"]).first()
        if pdfData:
            db.session.delete(pdfData)
            db.session.commit()
            return jsonify({'message': 'Pdf Removed'}), 201

        return jsonify({'message': 'Pdf Not Found'}), 401


@api.route('api/reset', methods=['GET', 'POST'])
@token_required
def reset_password(User):
    data = request.get_json()
    user = User.query.filter_by(email=User.email).first()
    if user:
        if check_password_hash(User.password, data['old']):
            password = generate_password_hash(data['new'], method='sha256')
            User.password = password
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
    user = User.query.filter_by(email=User.email).first()
    if user:
        if User.premium:
            User.change()
        else:
            return jsonify({'message': 'User without premium status'}), 401
    else:
        return jsonify({'message': 'User doesnt exist'}), 401
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
    user = User.query.filter_by(email=data['new']).first()
    if user:
        return jsonify({'message': 'Email already exists'}), 401
    else:
        user = User.query.filter_by(email=User.email).first()
        User.email = data['new']
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('api/change_username', methods=('POST',))
@token_required
def change_username(User):
    data = request.get_json()
    user = User.query.filter_by(email=User.email).first()
    new_user = User.query.filter_by(username=data['new']).first()
    if new_user:
        return jsonify({'message': 'Username already exists'}), 401
    else:
        User.username = data['new']
        db.session.commit()
        return jsonify(user.to_dict()), 201

    return jsonify({'message': 'Email doesnt exist'}), 401


@api.route('api/delete_user', methods=('POST',))
@token_required
def delete_user(User):
    data = request.get_json()
    if User.admin:
        user = User.query.filter_by(email=data['email']).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            return jsonify({'message': 'User doesnt exist'}), 401
    else:
        return jsonify({'message': 'User is not an admin'}), 401


@api.route("api/pdfMail", methods=('POST',))
@token_required
def sendPdf2Mail(User):
    request_data = json.loads(request.get_data())
    dirName = 'uploads/'+User.username+'/PDF_Files/'
    mimes = MimeTypes()
    msg = Message(subject=request_data["name"],
                  sender=current_app.config["MAIL_USERNAME"],
                  # replace with your email for testing
                  recipients=[request_data["mail"]],
                  body=request_data["message"])
    path_ = os.path.join(dirName, request_data["name"])
    with current_app.open_resource(path_) as fp:
        mime = mimes.guess_type(fp.name)
        msg.attach(path_, mime[0], fp.read())

    current_app.config["mail"].send(msg)
    response = {'msg': "sent"}
    return jsonify(response)
