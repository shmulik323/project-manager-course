import os
import tempfile
import unittest
import pytest
import run
import uuid
from run import app,db,User
import requests
TEST_DB = 'test.db'

class test_app(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)
 
    
    def tearDown(self):
        pass


    def register(self,name,last,username,email, password):
        new_user = User(public_id=str(uuid.uuid4()),name=name,last=last,
                    username=username, email=email, password=password, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return new_user
 
    def test_valid_user_registration(self):
        response = self.register('alex', 'vaitz','alexv', 'alex@gmail.com','alexv32')
        user = User.query.filter_by(username='alexv').first()
        self.assertEqual(user, response)
    
        

    def login(self, username, password):
        user=User.query.filter_by(username=username,password=password)
        if user:
            return True
        return False
    
    def test_login(self):
        """Make sure login and logout works."""

        response = self.login('alexv', 'alexv32')
        self.assertEqual(response,True)

        response = self.login('alexv' + 'x', 'alexv32')
        self.assertNotEqual(response,False)

        response = self.login( 'alexv', 'alexv32' + 'x')
        self.assertNotEqual(response,False)