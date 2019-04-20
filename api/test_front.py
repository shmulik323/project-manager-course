import os
import tempfile
import unittest
import urllib
from flask_testing import TestCase
from flask_testing import LiveServerTestCase
from selenium import webdriver
from api.application import create_app
from api.models import User, PremiumUser, db
from api.application import create_app
import requests
from flask import Flask, jsonify,Blueprint,abort, url_for
from flask_mail import Mail, Message
from flask_cors import CORS
from multiprocessing.pool import ThreadPool
import random, time, queue
import multiprocessing
from webdriver_manager.chrome import ChromeDriverManager



from multiprocessing.managers import BaseManager

test_user_first_name = "alex"
test_user_last_name = "vaitz"
test_user_username = "alexv32"
test_user_email = "alex@email.com"
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
            # Specify the test database
            SQLALCHEMY_DATABASE_URI='sqlite:///test.db',
            
            LIVESERVER_PORT=5000
        )
        
        return app

    def setUp(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('http://127.0.0.1:5000/')

        db.session.commit()
        db.create_all()

        # create test admin user
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen('http://127.0.0.1:5000/')
        self.assertEqual(response.code, 200)

class TestLogin(TestBase):
    
    def test_login(self):
       
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        assert url_for('pages.index') in self.driver.current_url

       
        #username_greeting = self.driver.find_element_by_id("username_greeting").text
        #assert "Hi, employee1!" in username_greeting
class TestLogout(TestBase):
    def test_logout(self):
        return
class TestRegister(TestBase):      
    def test_register(self):
        return
if __name__ == '__main__':
    unittest.main()