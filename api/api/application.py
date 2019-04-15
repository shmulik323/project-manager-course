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

    app.config["Mail_DEBUG"] = True
    app.config["Mail_USE_TLS"] = True
    app.config["Mail_DEBUG"] = True
    # EMAIL SETTINGS
    app.config["MAIL_SERVER"] = 'smtp.gmail.com'
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'shmulik323@gmail.com'
    app.config["MAIL_PASSWORD"] = 's0528481311'

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    from api.api import api
    app.register_blueprint(api, url_prefix="/")
    from api.models import db
    db.init_app(app)
    return app
