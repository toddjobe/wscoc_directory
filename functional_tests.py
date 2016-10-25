import wscoc_directory
from wscoc_directory.database import init_db


from flask import Flask
import unittest
import flask_testing
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By


class NewVisitorTestCase(flask_testing.LiveServerTestCase):
    EMAIL_LIST_NAMES = ['members', 'contacts', 'group1', 'group2', 'group3', 'group4', 'group5']
    #TESTING = true
    #SQLALCHEMY_DATABASE_URI = "sqlite://"

    def create_app(self):
        app = wscoc_directory.app
        app.config['TESTING'] = True
        init_db()
        return app


    def setUp(self):
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        self.browser  = webdriver.Firefox(capabilities=firefox_capabilities)
        self.browser.implicitly_wait(3)


        self.sample_directory = dict()
        for list_name in self.EMAIL_LIST_NAMES:
            with open('%s.txt' % list_name, 'r') as f:
                self.sample_directory[list_name] = f.read()



    def tearDown(self):
        self.browser.quit()

    def test_can_sync_up_email_lists(self):

        # Todd opens up the emailLists page
        self.browser.get(self.get_server_url()+'/email')

        # He sees the title has something to do with Walnut Street Church of Christ Email Directory
        title_regular_expression=r'Walnut\sSt(\.|reet)?\s[Cc](hurch\s)?[Oo](f\s)?C(hrist)?.+Email'
        self.assertRegexpMatches(self.browser.title, title_regular_expression)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertRegexpMatches(header_text, title_regular_expression)

        # He sees the boxes for entering groups (5 right now)
        # TODO: we can use find_elements_by_id perhaps
        # TODO: we can update the jinja2 template to use loop from context variable n_groups
        for i_group in range(1,5):
            textarea = self.browser.find_element_by_name('id_group_%d' % i_group)
            self.assertEqual(textarea.text, 'Enter Group %s email list.' % i_group)
            textarea = self.browser.find_element_by_name('label_group_%d' % i_group)
            self.assertEqual(textarea.text, 'Current Group %d email list' % i_group)

        # And a box for entering a master list
        textarea = self.browser.find_element_by_name('id_master')
        self.assertEqual(textarea.text, 'Enter master email list.')
        textarea = self.browser.find_element_by_name('label_master')
        self.assertEqual(textarea.text, 'Master email list')

        # And a box for entering the csv google email list
        textarea = self.browser.find_element_by_name('id_contacts')
        self.assertEqual(textarea.text, 'Enter contacts email list.')
        textarea = self.browser.find_element_by_name('label_contacts')
        self.assertEqual(textarea.text, 'Contact email list')

        # There's a submit box that's clickable
        submit_button = self.browser.find_element_by_name('id_submit')
        self.assertEqual(submit_button.text, 'Submit')
        self.assertTrue(submit_button.is_enabled())


        # He enters some emails in the master text box and all group text boxes.
        textarea = self.browser.find_element_by_name('id_master')
        textarea.clear()
        textarea.send_keys(self.sample_directory['members'])

        textarea = self.browser.find_element_by_name('id_contacts')
        textarea.clear()
        textarea.send_keys(self.sample_directory['contacts'])

        for i_group in range(1,5):
            textarea = self.browser.find_element_by_name('id_group_%d' % i_group)
            textarea.clear()
            textarea.send_keys(self.sample_directory['group%d' % i_group])


        # He then presses the submit button
        submit_button.click()

        # He's redirected to a new page
        # He sees the title has something to do with Fixed
        title_regular_expression=r'Fixed'
        WebDriverWait(self.browser,10).until(EC.title_contains(title_regular_expression))
        self.assertRegexpMatches(self.browser.title, title_regular_expression)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertRegexpMatches(header_text, title_regular_expression)

        # Each group box has textboxes highlighting extra entries.
        for i_group in range(1,5):
            #textarea = self.browser.find_element_by_name('id_group%d_extra' % i_group)
            textarea = self.browser.find_element_by_name('id_group%d_extra_label' % i_group)
            self.assertEqual(textarea.text, 'Extra Group %d emails' % i_group)

        self.fail('Implement the rest of the the tests.')

        # And there's a text box for a 'fixed' list in each group that will be in sync with the master list
        # But right now it's empty
        for i_group in range(1,5):
            textarea = self.browser.find_element_by_name('id_group_intersect_%d' % i_group)
            self.assertEqual(textarea.text)
            textarea = self.browser.find_element_by_name('label_group_intersect_%d' % i_group)
            self.assertEqual(textarea.text, 'Fixed Group %d emails' % i_group)

        # There's an unassigned text box that is also empty
        for i_group in range(1,5):
            textarea = self.browser.find_element_by_name('id_unassigned')
            self.assertFalse(textarea.text)
            textarea = self.browser.find_element_by_name('label_unassigned')
            self.assertEqual(textarea.text, 'Unassigned email list')

        self.fail('Implement the rest of the the tests.')



    def test_can_export_existing_contacts(self):
        # Terry has heard that you can view the directory easily from the web.
        # He goes to checkout the homepage
        self.browser.get(self.get_server_url())

        # he sees the title has something to with the Walnut Street Church of Christ and a Directory and the page header is the same
        title_regular_expression =r'Walnut\sSt(\.|reet)?\s[Cc](hurch\s)?[Oo](f\s)?C(hrist)?.+[Dir](\s|\.|ectory){1}'
        self.assertRegexpMatches(self.browser.title, title_regular_expression)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertRegexpMatches(header_text, title_regular_expression)

        # If his authorization has expired he's redirected to an OAuth window


        self.browser.find_element_by_xpath("//span[.='Google']").click()
        #self.fail('Finish functional tests.')
        '''
        self.browser.find_element(By.ID, "Email").send_keys('...')
        self.browser.find_element(By.ID, "next").click()
        self.browser.find_element(By.ID, "Passwd").send_keys('...')
        self.browser.find_element(By.ID, "signIn").click()
        self.browser.find_element(By.ID, "nav-questions")
        '''



        # Once authorized he sees a view of all the walnut street church of christ groups.

        # He sees an option to edit his current contacts.  He wants to do that.

        # This redirects him to his google contacts page whereupon he can change things and then get back to the original server

        # He sees an option to export locally in word, csv, and pdf or submit to a ('fake') wordpress server.

        # He exports locally

        # He opens the local files and sees that his changes have been updated.

        # He selects export to the server and then is asked for his username/password creds.

        # He checks the wordpress url to see that his changes have indeed resulted in updates.

        # Satisfied, he goes back to sleep



if __name__ == '__main__':
    unittest.main()