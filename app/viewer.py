# api.py

# ## Imports

from flask import url_for, abort, jsonify, request, render_template
from flask.ext.cors import cross_origin
from app import app
from app import models
from app import db
from app import errors
from app import controller
from controller import fetch_movies, fetch_movie

from error_displayer import InvalidUsage
from models import MovieLocation
import urllib2

from werkzeug.contrib.cache import SimpleCache  # production: MemcachedCache

# ## Caching

cache = SimpleCache()  # production: cache = MemcachedCache(['...'])

CLIENT_CACHE_TIMEOUT = 300
SERVER_CACHE_TIMEOUT = 300

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handles an error caused by invalid usage of the API.

    Arguments:
    - `error`: the error to handle.
    """

    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def handle_invalid_resource_path(error):
    """Handles requests to invalid resource paths.

    Arguments:
    - `error`: the error to handle.
    """

    response = jsonify({'error': {'status_code': 404,
                                  'message': 'No resource behind the URI'}})
    response.status_code = 404
    return response

@app.before_request
def return_cached():
    """Checks if the request is already cached."""

    if not request.values:
        response = cache.get(request.path)
        if response:
            return response


@app.after_request
def cache_response(response):
    """Caches a response.

    Arguments:
    - `response`: the request response to cache.
    """

    STATUS_OK = 200

    if not request.values and response.status_code == STATUS_OK:
        cache.set(request.path, response, SERVER_CACHE_TIMEOUT)
    return response


@app.after_request
def add_header(response):
    """Adds extra headers to the response.

    Arguments:
    - `response`: the response to be augmented.
    """

    response.cache_control.max_age = CLIENT_CACHE_TIMEOUT
    return response


# ## Documentation page

@app.route('/sfmovies/api/v1/', methods=['GET'])
@app.route('/sfmovies/api/v1/docs', methods=['GET'])
def get_documentation():
    """Returns a documentation page of the API."""
    return render_template("docs.html")

# ## Main page

@app.route('/', methods=['GET'])
def get_root_dir():
    return render_template("index.html");

# ## Resources

@app.route('/sfmovies/api/v1/movies', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def get_movies():
    """Returns a JSON representation of the locations of movies shot in San
    Francisco."""
    parameters = {}

    # Get parameters
    if request.method == 'GET':
        arguments = request.args.items()
        for arg in arguments:
            parameters[arg[0]] = arg[1]

    print parameters
    return jsonify({'movies': controller.fetch_movies(parameters)})

@app.route('/sfmovies/api/v1/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    Arguments:
    - `movie_id`: the id of the movie to be retrieved.
    """
    movie = controller.fetch_movie(movie_id);

    if movie is None:
        raise InvalidUsage('No movie with id = ' + str(movie_id),
                           status_code=404,
                           payload={'links': [
                               {'href': '/api/v1/movies/' + str(movie_id),
                                'rel': 'self'}
                           ]})
    return jsonify({'movie': movie})
