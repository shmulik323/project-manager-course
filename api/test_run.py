import os
import tempfile
import unittest
from flask_testing import TestCase
from api.models import User, PremiumUser,db
from api.application import create_app
import requests
from flask import Flask, jsonify,Blueprint,abort, url_for,json
from flask_mail import Mail, Message
from flask_cors import CORS


class TestBase(TestCase):
    
    def create_app(self):
        
        # pass in test configurations
        config_name = 'testing'
        app=create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
            
        )
        return app

    def setUp(self):
        self.client=create_app().test_client()
        db.session.commit()
        db.drop_all()
        db.create_all()
       
        user = User(email='alex@gmail.com',password='alexv32',name='alex',last='vaitz',username='alexv')

        premium = PremiumUser(email='almog@gmail.com', password='almog32',name='almog', last='gro', username='almoggr')
        premium.change()

        db.session.add(user)
        db.session.add(premium)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class Test_Models(TestBase):
    def test_valid_user_registration(self):
        
        self.assertEqual(User.query.count(),2)


    def test_unique_accounts(self):
        user = User.query.filter_by(email='alex@gmail.com').first()
        
        premium = User.query.filter_by(username='almog@gmail.com').first()

        self.assertNotEqual(user, premium)

class Test_Functionality(TestBase):
    def test_login(self):
        with self.app.test_client() as client:
            user = User.query.filter_by(email='alex@gmail.com').first()
            response=self.client.post('api/auth/login',data={'email':user.email,'password':'alexv32'},follow_redirects=True)
            self.assertEqual(response.status_code,200)

if __name__ == "__main__":
    unittest.main()
