import unittest
import time
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from flask import url_for
from flask_testing import LiveServerTestCase

from app import app, db

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

TEST_DB = 'test.db'

class FlaskrFrontEndTestBase(LiveServerTestCase):
    def create_app(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        app.config.update(
          LIVESERVER_PORT=8000
        )

        return app

    def setUp(self):
        """Setup the test driver"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get('http://localhost:%s' % 5000)

        """Set up a blank temp database before each test"""
        db.session.commit()
        db.create_all()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()
        self.driver.quit()

class TestLogin(FlaskrFrontEndTestBase):

    def test_login_final_user(self):
        login_link = self.get_server_url() + url_for('login')

        self.driver.get(login_link)
        self.driver.find_element_by_name("username").send_keys('admin')
        self.driver.find_element_by_name("password").send_keys('admin')
        self.driver.find_element_by_css_selector('.btn.btn-primary').click()

        time.sleep(1)

        welcome_message = self.driver.find_element_by_css_selector("flash.alert.alert-success.col-sm-4").text
        assert "You were logged in" in welcome_message

if __name__ == '__main__':
    unittest.main()
