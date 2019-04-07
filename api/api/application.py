"""
application.py  
- creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_cors import CORS


def create_app(app_name='API'):
    UPLOAD_FOLDER = './uploads'
    app = Flask(app_name, static_folder="../../client/.nuxt/dist/server",
                template_folder="../../client/.nuxt/dist/server")
    app.config.from_object('api.config.BaseConfig')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    from api.api import api
    app.register_blueprint(api, url_prefix="/")
    from api.models import db
    db.init_app(app)
    return app
