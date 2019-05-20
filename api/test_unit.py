import os
import tempfile
import unittest
import urllib
import selenium
from selenium import webdriver
from api.application import create_app
from api.models import User, PremiumUser, db
from api.application import create_app
import requests
from flask import Flask, jsonify,Blueprint,abort, url_for
from flask_mail import Mail, Message
from flask_cors import CORS
from multiprocessing.pool import ThreadPool
from flask_testing import TestCase
import random, time, queue
import multiprocessing
from webdriver_manager.chrome import ChromeDriverManager

test_user_first_name = "alex"
test_user_last_name = "vaitz"
test_user_username = "alexv111"
test_user_email = "alexv@gmail.com"
test_user_password = "alex1234"

test_user2_first_name = "mishel"
test_user2_last_name = "elgawi"
test_user2_username = "mishel11"
test_user2_email = "mishel@email.com"
test_user2_password = "mishel1234"

class TestBase(TestCase):
    
    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            

            LIVESERVER_PORT=3000
        )
        
        return app

    def setUp(self):
        chromeOptions = webdriver.ChromeOptions()
        
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument("--start-fullscreen")
        chromeOptions.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.driver.get('http://127.0.0.1:5000/')
        self.driver.maximize_window()
        db.session.commit()
        db.create_all()


        db.session.commit()

    def tearDown(self):
        self.driver.quit()

class TestFileOptions(TestBase):
    
    def test_premiun(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        self.user.change()
        db.session.add(self.user)
        db.session.commit()
    
        assert User.query.filter_by(email=test_user_email).first

    def test_admin(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        self.user.change()
        self.user.promote()
        db.session.add(self.user)
        db.session.commit()
        
        assert User.query.filter_by(email=test_user_email).first

    def test_user(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
    
        assert User.query.filter_by(email=test_user_email).first

if __name__ == '__main__':
    unittest.main()