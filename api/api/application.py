"""
application.py
- creates a Flask app instance and registers the database object
"""

from flask import Flask, Blueprint, jsonify, request, current_app, render_template, Response
from flask_mail import Mail, Message
from flask_cors import CORS
import json


def create_app(app_name='API'):
    UPLOAD_FOLDER = './uploads'
    app = Flask(app_name, static_folder="../../client/.nuxt/dist/server",
                template_folder="../../client/.nuxt/dist/server")
    app.config.from_object('api.config.BaseConfig')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'mishel110393@gmail.com',
        "MAIL_PASSWORD": 'Spygame326'
    }

    app.config.update(mail_settings)
    mail = Mail(app)

    @app.route("/api/Sent", methods=('POST',))
    def index():
        request_data = json.loads(request.get_data())
        msg = Message(subject=request_data["name"],
                      sender=app.config.get("MAIL_USERNAME"),
                      # replace with your email for testing
                      recipients=[request_data["dev"]],
                      body=request_data["message"])
        mail.send(msg)
        response = {'msg': "Hello"}
        return jsonify(response)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    from api.api import api
    app.register_blueprint(api, url_prefix="/")
    from api.admin import admin
    app.register_blueprint(admin)
    from .models import db, User, Pdf

    db.init_app(app)
    return app
