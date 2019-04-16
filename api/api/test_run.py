import os
from form import ContactForm
import tempfile
import unittest
import uuid
from models import db,User, PremiumUser
from application import create_app
import requests
from flask import Flask, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
TEST_DB = 'test.db'

class test_app(unittest.TestCase):
    def setUp(self):
        app=create_app()
        app.config.from_object('config.BaseConfig')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        
        self.app = app.test_client()
       

        self.assertEqual(app.debug, False)

    def register(self, name, last, username, email, password):
        new_user = User(email=email, password=password,name=name, last=last,
                               username=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def register_premium(self, name, last, username, email, password):
        new_user = PremiumUser(email=email, password=password,name=name, last=last,
                               username=username)
        new_user.change()
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def test_valid_user_registration(self):
        response = self.register(
            'alex@gmail.com', 'alexv32','alex', 'vaitz', 'alexv')
        user = User.query.filter_by(username='alexv').first()
        self.assertEqual(user, response)

    def test_valid_premium_registration(self):
        response = self.register_premium(
            'almog@gmail.com', 'almog32','almog', 'gro', 'almoggr')
        user = User.query.filter_by(username='almoggr').first()
        self.assertEqual(user, response)

    def test_unique_accounts(self):
        response = self.register(
            'alex@gmail.com', 'alexv32','alex', 'vaitz', 'alexv')
        user = User.query.filter_by(username='alexv').first()
        premium_response = self.register_premium(
            'almog@gmail.com', 'almog32','almog', 'gro', 'almoggr')
        premium = User.query.filter_by(username='almoggr').first()
        self.assertNotEqual(user, premium)

    def login(self, username, password):
        user = User.query.filter_by(username=username, password=password)
        if user:
            return True
        return False

    def test_login(self):
        """Make sure login and logout works."""

        response = self.login('alexv', 'alexv32')
        self.assertEqual(response, True)

        response = self.login('alexv' + 'x', 'alexv32')
        self.assertNotEqual(response, False)

        response = self.login('alexv', 'alexv32' + 'x')
        self.assertNotEqual(response, False)


if __name__ == "__main__":
    unittest.main()
