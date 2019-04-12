"""
application.py  
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_mail import Mail, Message
from flask_cors import CORS
import os


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
        "MAIL_USERNAME": 'your email',
        "MAIL_PASSWORD": 'your password'
    }

    app.config.update(mail_settings)
    mail = Mail(app)


    @app.route("/")
    def index():
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["mishel326@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
        response = {'msg': "Hello"}
        return jsonify(response)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    from api.api import api
    app.register_blueprint(api, url_prefix="/")
    from api.models import db
    db.init_app(app)
    return app
