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
from app import controller
from app.controller import fetch_movies, fetch_movie

# # Classes


class APITestCase(unittest.TestCase):

    # ## Scaffolding

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ## Tests

    def test_get_movies(self):
        parameters = {}
        movies = fetch_movies(parameters);
        assert movies[0]['actor_1'] == "Siddarth"
        assert movies[1]['latitude'] == 37.7918653     
        assert movies[2]['location'] == "Justin Herman Plaza"

    def test_get_movies_with_fields(self):
        parameters = {'fields': u'title,year'}
        movies = fetch_movies(parameters)
        assert movies[0]['title'] == "180"
        assert movies[0]['year'] == 2011
        assert movies[1]['links'][0]['href'] == "/api/v1/movies/2"

    def test_get_movies_with_year_and_title(self):
        parameters = {'year': u'2011', 'title': u'180'}
        movies = fetch_movies(parameters)
        assert movies[0]['latitude'] == 37.7992627
        assert movies[0]['longitude'] == -122.3976732
        assert movies[1]['latitude'] == 37.7918653

    def test_get_movies_with_sort_and_limit(self):
        parameters = {'sort': u'year', 'limit': u'5'}
        movies = fetch_movies(parameters)
        assert movies[0]['year'] == 2015
        assert movies[1]['writer'] == "Marielle Heller"

    def test_get_movies_with_sort_and_offset(self):
        parameters = {'sort': u'year', 'offset': u'1'}
        movies = fetch_movies(parameters)
        assert movies[2]['actor_1'] == "Alexander Skarsgard"

    def test_get_one_movie_by_id(self):
        movie = fetch_movie(888)
        assert movie["writer"] == "Marielle Heller"
