# tests/test_api.py

# # Imports

import os
import unittest
import urllib2
import json

from config import BASE_DIR
from app import app
from app import models
from app import error_displayer
from app import viewer

# # Classes


class APITestCase(unittest.TestCase):

    # ## Scaffolding

    def setUp(self):
        self.app = app.test_client()
        self.baseUrl = "http://localhost:5000/sfmovies/api/"

    def tearDown(self):
        pass

    # ## Tests

    # ### API Version 1 tests

    # GET /moviesnotthere

    def test_v1_moviesnotthere_should_have_error_message(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/moviesnotthere")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['message'] == "No resource behind the URI"


    def test_v1_movie_year_eq_horse_should_give_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?year=horse")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400

    def test_v1_movie_year_gt_helicopter_should_give_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?year>=helicopter")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400

    # errors

    def test_v1_latitude_eq_horse_should_raise_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?latitude=horse")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400

    def test_v1_longitude_eq_foo_should_raise_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?longitude=foo")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400

    def test_v1_movies_wrong_field_should_raise_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?fields=title,baz")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400


    def test_v1_movies_limit_invalid_value_should_raise_error(self):
        try:
            urllib2.urlopen(self.baseUrl + "v1/movies?limit=foobar")
            assert False  # Should not get here
        except Exception as e:
            response = json.loads(e.read())
            assert response['error']['status_code'] == 400
