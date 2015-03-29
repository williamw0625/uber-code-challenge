# tests/test_models.py

# # Imports

import os
import unittest

from app import models

# # Classes


class ModelsTestCase(unittest.TestCase):

    # ## Scaffolding

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # ## Tests

    def test_model_greed_should_have_actor_zasu_pitts(self):
        greed = models.MovieLocation(
            title='Greed',
            year=1924,
            location='Hayes Street at Laguna',
            fun_fact='',
            production_company='Metro-Goldwyn-Mayer (MGM)',
            distributor='Metro-Goldwyn-Mayer (MGM)',
            director='Eric von Stroheim',
            writer='Eric von Stroheim',
            actor_1='Zasu Pitts Rep',
            actor_2='',
            actor_3='Cloris Leachman',
            latitude=37.7764647,
            longitude=-122.4262985)
        assert greed.actor_1 == 'Zasu Pitts Rep'

    def test_model_vertigo_should_have_year_director_alfred_hitchcock(self):
        vertigo = models.MovieLocation(
            title="Vertigo",
            year=1958,
            location="San Francisco Drydock (20th and Illinois Streets)",
            fun_fact="",
            production_company="Alfred J. Hitchcock Productions",
            distributor="Paramount Pictures",
            director="Alfred Hitchcock",
            writer="Alec Coppel",
            actor_1="James Stewart",
            actor_2="Kim Novak",
            latitude=37.7561141,
            longitude=-122.3871395)
        assert vertigo.director == 'Alfred Hitchcock'
