import os
from flask import Flask
from flask_testing import TestCase
from selenium import webdriver
import unittest
import urllib2

class NewVisitorTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.browser = webdriver.Firefox()

        '''
        self.db_fd, wscoc_directory.app.config['DATABASE'] = wscoc_directory.database.init_db()
        wscoc_directory.app.config['TESTING'] = True
        self.app = wscoc_directory.app.test_client()
        with wscoc_directory.app.app_context():
            wscoc_directory.init_db()
        '''
    def tearDown(self):
        self.browser.quit()

        '''
        os.close(self.db_fd)
        os.unlink(wscoc_directory.app.config['DATABASE'])
        '''
    def test_server_is_up_and_running(self):
        response = urllib2.urlopen('http://localhost:5000')
        self.assertEqual(response.code, 200)

    def test_can_start_a_new_entry_retrieve_it_later(self):
        # Terry has heard that you can view the directory easily from the web.
        # He goes to checkout the homepage
        self.browser.get('http://localhost:8000')

        # he sees the title has something to do with the directory
        self.assertIn('Walnut Street Church of Christ Directory', self.browser.title)
        self.fail('Finish the test!')
        # He's invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep



if __name__ == '__main__':
    unittest.main()