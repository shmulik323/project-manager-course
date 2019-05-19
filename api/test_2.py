import os
import tempfile
import unittest
import urllib
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
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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
        options.setBinary('C:\Program Files (x86)\Google\Chrome\Application')
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.driver.get('http://127.0.0.1:3000/')
        self.driver.maximize_window()
        db.session.commit()
        db.create_all()


        db.session.commit()

    def tearDown(self):
        self.driver.quit()

class TestFileOptions(TestBase):
    def test_spmp(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/create')
        time.sleep(2)

        self.driver.find_element_by_id("spmp").click()
        time.sleep(2)

        assert self.driver.find_element_by_id("spmp")
    
    def test_srs(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/create')
        time.sleep(2)

        self.driver.find_element_by_id("srs").click()
        time.sleep(2)

        assert self.driver.find_element_by_id("spmp")

    def test_download(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/create')
        time.sleep(2)

        self.driver.find_element_by_id("srs").click()
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
        time.sleep(1)
        self.driver.find_element_by_id("download_pdf").click()
        time.sleep(2)

        assert self.driver.find_element_by_id("spmp")
    
    def test_search_category(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/search')
        time.sleep(2)  

        self.driver.find_element_by_id("start_search").click()
        time.sleep(3) 

        assert self.driver.find_element_by_id("sort_button") 
    

    def test_search_name(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/search')
        time.sleep(2)  

        self.driver.find_element_by_id("name").send_keys("cool stuff")
        time.sleep(1)
        self.driver.find_element_by_id("start_search").click()
        time.sleep(3) 

        assert self.driver.find_element_by_id("sort_button")

    def test_search_date(self):
        User.query.delete()
        self.user = User(email=test_user_email,password=test_user_password,name=test_user_first_name,last=test_user_last_name,username=test_user_username)
        db.session.add(self.user)
        db.session.commit()
        time.sleep(1)
        self.driver.find_element_by_id("login_link").click()
        time.sleep(3)

        self.driver.find_element_by_id("email").send_keys(test_user_email)
        self.driver.find_element_by_id("password").send_keys(test_user_password)
        self.driver.find_element_by_id("login_click").click()
        time.sleep(2)
        self.driver.get('http://127.0.0.1:3000/search')
        time.sleep(2)  

        self.driver.find_element_by_id("start_search").click()
        time.sleep(3)

        assert self.driver.find_element_by_id("sort_button")

if __name__ == '__main__':
    unittest.main()