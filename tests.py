import wscoc_directory
import unittest
import flask_testing
import json

'''
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
'''

class WscocDirectoryTest(flask_testing.TestCase):

    render_templates = False
    MASTER_EMAIL_LIST = ['toddjobe@gmail.com', 'arj.sunraes@gmail.com', 'rebobjobe@gmail.com', 'blah@blah.com', 'fake@fake.com', 'more@more.com', 'less@less.com']

    def create_app(self):
        app = wscoc_directory.app
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.email_lists_good = dict(
            master='\n'.join(self.MASTER_EMAIL_LIST),
            contacts='\n'.join(self.MASTER_EMAIL_LIST + ['csvOnly@csvOnly.com']),
            group1=self.MASTER_EMAIL_LIST[0],
            group2=self.MASTER_EMAIL_LIST[1],
            group3=self.MASTER_EMAIL_LIST[2],
            group4=self.MASTER_EMAIL_LIST[3],
            group5='\n'.join([self.MASTER_EMAIL_LIST[4],'extra@extra.com']),
            group1_extra='',
            group2_extra='',
            group3_extra='',
            group4_extra='',
            group5_extra='extra@extra.com',
            contacts_extra='csvOnly@csvOnly.com',
            contacts_missing='',
            unassigned='\n'.join(sorted(set(self.MASTER_EMAIL_LIST[5:])))
        )

    def tearDown(self):
        pass

    def test_root_url_is_active(self):
        # sends HTTP GET request to the application
        # on the specified path
        response = self.client.get('/')

        # assert the status code of the response
        self.assertEqual(response.status_code, 200)

    def test_index_returns_correct_html(self):
        self.client.get('/')
        self.assert_template_used('layout.html')

    def test_email_url_is_active(self):
        response = self.client.get('/email')

        # assert the status code of the response
        self.assertEqual(response.status_code, 200)


    def test_post_to_fixed(self):
        arg_dict = dict(
            id_master=self.email_lists_good['master'],
            id_contacts=self.email_lists_good['contacts'],
            id_group_1=self.email_lists_good['group1'],
            id_group_2=self.email_lists_good['group2'],
            id_group_3=self.email_lists_good['group3'],
            id_group_4=self.email_lists_good['group4'],
            id_group_5=self.email_lists_good['group5']
        )
        extras = [{
            'label_id': 'id_group%d_extra_label' % i,
            'textarea_id': 'id_group%d_extra' % i,
            'id': '%d' % i,
            'text': self.email_lists_good['group%d_extra' % i]
        } for i in range(1, 6)]
        unassigned = {'text': self.email_lists_good['unassigned']}
        contacts_extra = {'text': self.email_lists_good['contacts_extra']}
        contacts_missing = {'text': self.email_lists_good['contacts_missing']}
        result = self.client.post('/fixed', data=arg_dict)

        self.assert200(result)
        self.assert_template_used('fixed.html')
        self.assert_context("extras", extras)
        self.assert_context("unassigned", unassigned)
        self.assert_context("contacts_missing", contacts_missing)
        self.assert_context("contacts_extra", contacts_extra)


    def test_collision_of_group_lists(self):
        pass


if __name__ == '__main__':
    unittest.main()