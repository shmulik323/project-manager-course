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
from selenium.webdriver.support.ui import Select


from multiprocessing.managers import BaseManager

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
            # Specify the test database

            LIVESERVER_PORT=3000
        )
        
        return app

    def setUp(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('http://127.0.0.1:3000/')
        
        db.session.commit()
        db.create_all()


        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    #def test_server_is_up_and_running(self):
        #response = urllib.request.urlopen('http://127.0.0.1:3000/')
        #self.assertEqual(response.code, 200)

class TestRegister(TestBase):      
    def test_register(self):
        self.driver.find_element_by_id("register").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user2_email)
        self.driver.find_element_by_id("username").send_keys(
            test_user2_username)
        self.driver.find_element_by_id("first").send_keys(
            test_user2_first_name)
        self.driver.find_element_by_id("last").send_keys(
            test_user2_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_user2_password)
        self.driver.find_element_by_id("reg").submit()
        time.sleep(2)

        self.driver.find_element_by_id("logout").click()
        time.sleep(2)

        assert self.driver.find_element_by_id("register")

class TestLogin(TestBase):
    
    def test_login(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.find_element_by_id("logout").click()
        time.sleep(2)

        assert self.driver.find_element_by_id("login_link")
        
class TestSideBar(TestBase):
    def test_profile(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        assert self.driver.find_element_by_id("fetch")

    def test_contact(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/contact')
        time.sleep(2)

        self.driver.find_element_by_id("subject").send_keys('error in something')
        
        self.driver.find_element_by_id("message").send_keys('i have a lot of errors in a lot of places please help.')
        time.sleep(1)
        assert self.driver.find_element_by_id("submit")
    
    def test_contact_manager(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/contact_manager')
        time.sleep(2)

        self.driver.find_element_by_id("subject").send_keys('I have an issue')
        
        self.driver.find_element_by_id("message").send_keys('i have a lot of problems in a lot of places please help.')
        time.sleep(1)
        assert self.driver.find_element_by_id("submit")

    def test_create(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/create')
        time.sleep(2)

        self.driver.find_element_by_id("pdf")

class TestProfileFunctions(TestBase):
    def test_reset_password(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("reset_password").click()
        time.sleep(2)

        self.driver.find_element_by_id("old_pass").send_keys(test_user_password)
        self.driver.find_element_by_id("new_pass").send_keys('aaabbbccc1234')
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()

        assert self.driver.find_element_by_id("logout")
    
    def test_change_email(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("change_email").click()
        time.sleep(2)

        self.driver.find_element_by_id("old_email").send_keys(test_user_email)
        self.driver.find_element_by_id("new_email").send_keys('alex1234@gmail.com')
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()

        assert self.driver.find_element_by_id("logout")
    
    def test_change_username(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("change_username").click()
        time.sleep(2)

        self.driver.find_element_by_id("old_user").send_keys(test_user_username)
        self.driver.find_element_by_id("new_user").send_keys('alex12345')
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()

        assert self.driver.find_element_by_id("logout")

    def test_change_picture(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("change_picture").click()
        time.sleep(2)
        assert self.driver.find_element_by_id("logout")
    
    def test_edit_profile(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("change_profile").click()
        time.sleep(2)

        self.driver.find_element_by_id("first").send_keys('alexander')
        self.driver.find_element_by_id("last").send_keys('vitzi')
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()

        assert self.driver.find_element_by_id("logout")
    
    def test_cancel_premium(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
       
        db.session.add(self.user)
        
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(1)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)

        self.driver.get('http://127.0.0.1:3000/profile')
        time.sleep(2)
        self.driver.find_element_by_id("cancel_premium").click()
        time.sleep(2)
        self.driver.find_element_by_id("email")
        self.driver.find_element_by_id("email").send_keys(test_user_email)
        time.sleep(1)
        self.driver.find_element_by_id("submit").click()

        assert self.driver.find_element_by_id("logout")

if __name__ == '__main__':
    unittest.main()