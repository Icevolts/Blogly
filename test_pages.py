from unittest import TestCase
from models import User
from app import app

class PageTestCase(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_create_user(self):
        with self.client:
            res = self.client.post('/users/new', data = {'first_name': 'Gerald', 'last_name': 'Walters', 'image_url': 'None'})
        self.assertEqual(res.status_code,302)
        self.assertEqual(res.location,'/users')

    def test_delete_user(self):
        with self.client:
            user_id = 9999
            res = self.client.post(f'/users/{user_id}/delete')
        self.assertEqual(res.status_code,404)
    