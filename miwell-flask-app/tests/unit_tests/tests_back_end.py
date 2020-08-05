# A new take on tests_back_end.py.

import unittest

import os

import time

from flask import url_for, abort
from flask_testing import TestCase

from flaskr import create_app, db
from flaskr.register.models import Patient, Psychiatrist

from tests.CustomLiveServerTestCase import LiveServerTestCase

from flask_argon2 import generate_password_hash  # For generating password hashes.


# Test 1 - Test our models. ----------------------------------------------------------------------------

# The first class has methods to test that each of the models in the app are working as expected.
# This is done by querying the database to check that the correct number of records exist in each table.

class TestModels(LiveServerTestCase):

    def test_patient_model(self):  # Test number of records in our Patient table.
        fields_count = Patient.query.count()
        self.assertEqual(fields_count, 9)

    def test_psych_model(self):  # Test number of records in our Psychiatrist table.
        fields_count = Psychiatrist.query.count()
        self.assertEqual(fields_count, 9)


# Test 2a - Test our pages. ----------------------------------------------------------------------------

# The second class has methods to test access to each page, to ensure the expected status code is returned.
# For non-restricted views, such as the homepage and the login page, the 200 OK code should be returned
# For restricted views that require authenticated access, a 302 Found code is returned.

class TestPages(LiveServerTestCase):

    def test_homepage_view(self):  # Test that homepage is accessible without a login.

        http_response = self.client.get(url_for('main_bp.homepage'))
        self.assertEqual(http_response.status_code, 200)

    def test_about_view(self):  # Test that login page is accessible without login.
        http_response = self.client.get(url_for('main_bp.about'))
        self.assertEqual(http_response.status_code, 200)

    def test_logout_view(self):  # Test that logout link is inaccessible without login, and redirects them back home.

        target_url = url_for('auth_bp.logout')
        redirect_url = url_for(url_for('main_bp.homepage'), next=target_url)
        http_response = self.client.get(target_url)
        self.assertEqual(http_response.status_code, 302)
        self.assertRedirects(http_response, redirect_url)

    def test_dashboard_view(self):  # Test that dashboard is inaccessible without login, and redirects back home.
        target_url = url_for('dashboard_bp.dashboard')
        redirect_url = url_for('main_bp.homepage', next=target_url)
        http_response = self.client.get(target_url)
        self.assertEqual(http_response.status_code, 302)
        self.assertRedirects(http_response, redirect_url)


# Test 2b - Test error pages. ----------------------------------------------------------------------------

# The third class has methods to ensure that the error pages are shown when the respective error occurs.

class TestErrorPages(LiveServerTestCase):

    def test_403_forbidden(self):
        http_response = self.client.get('/403')
        self.assertEqual(http_response.status_code, 403)
        self.assertTrue("403 Error" in http_response.data)

    def test_404_not_found(self):
        http_response = self.client.get('/nothinghere')
        self.assertEqual(http_response.status_code, 404)
        self.assertTrue("404 Error" in http_response.data)

    def test_500_internal_server_error(self):
        http_response = self.client.get('/500')
        self.assertEqual(http_response.status_code, 500)
        self.assertTrue("500 Error" in http_response.data)


if __name__ == '__main__':
    unittest.main()
