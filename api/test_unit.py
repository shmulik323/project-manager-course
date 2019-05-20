import os
import tempfile
import unittest
import urllib
from api.models import User, PremiumUser, db
from api.application import create_app
import requests
from flask import Flask, jsonify,Blueprint,abort, url_for
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_testing import TestCase

test_user_first_name = "alex"
test_user_last_name = "vaitz"
test_user_username = "alexv111"
test_user_email = "alexv@gmail.com"
test_user_password = "alex1234"


class UnitTesting(unittest.TestCase):

    def setUp(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            LIVESERVER_PORT=3000
        )
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.commit()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        User.query.delete()

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()