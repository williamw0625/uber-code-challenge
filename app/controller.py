# ## Imports

from flask import url_for, abort, jsonify, request, render_template
from flask.ext.cors import cross_origin
from app import app
from app import models
from app import db
from app import errors
from errors import InvalidUsage
from models import MovieLocation
import urllib2

PROPERTIES = ['id', 'title', 'writer', 'actor_1', 'actor_2', 'actor_3',
              'director', 'distributor', 'production_company', 'location',
              'year', 'fun_fact', 'latitude', 'longitude']

KEYWORDS = ['sort', 'fields', 'limit', 'offset']

def sort_query_result(query, parameters):
    sort_field = parameters['sort']

    if sort_field.startswith('-'):
        sort_field = sort_field[1:]

    if sort_field not in PROPERTIES:
        raise_invalid_message('sort : ' + format(sort_field));

    model_field = getattr(MovieLocation, sort_field, None)
    return query.order_by(model_field.desc())

def fields_query_result(query, parameters):
    fields = parameters['fields'].split(",")

    for field in fields:
        if field not in PROPERTIES:
            raise_invalid_message('fields : ' + format(field));

        model_field = getattr(MovieLocation, field, None)
        query = query.add_column(model_field)

    return query.add_column(MovieLocation.id)

def limit_query_result(query, parameters):
    limit = parameters['limit']
    
    try:
        int(limit)
    except:
        raise_invalid_message('limit : ' + format(limit))

    return query.limit(limit)

def offset_query_result(query, parameters):
    offset = parameters['offset']

    try:
        int(offset)
    except:
        raise_invalid_message('offset :' + format(offset))

    return query.offset(parameters['offset'])

def default_query_result(query, parameter, parameterValue):

    if parameter.endswith('<') or parameter.endswith('>'):
        less_or_greater_than = parameter[-1]
        parameter = parameter[:-1]
        check_property_type(parameter, parameterValue, PROPERTIES)
        modelValue = getattr(MovieLocation, parameter, None)

        if less_or_greater_than == '>':
            return query.filter(modelValue >= parameterValue)
        else:
            return query.filter(modelValue <= parameterValue)

    else:
        check_property_type(parameter, parameterValue, PROPERTIES)
        modelValue = getattr(MovieLocation, parameter, None)
        return query.filter(modelValue == parameterValue)

def fetch_movies(parameters):

    """Returns a JSON representation of the locations of movies shot in San
    Francisco."""

    query = MovieLocation.query

    # filter
    for parameter in parameters:
        # ignore sort, field, limit and offset
        if parameter in KEYWORDS:
            continue
        
        print parameter
        value = parameters[parameter]
        query = default_query_result(query, parameter, value)

    # sort
    if 'sort' in parameters:
        query = sort_query_result(query, parameters)
    else:
        query = query.order_by('id')

    # fields
    if 'fields' in parameters:
        query = fields_query_result(query, parameters)

    # paging
    if 'limit' in parameters:
        query = limit_query_result(query, parameters)

    if 'offset' in parameters:
        query = offset_query_result(query, parameters)

    movies = query.all()
    movies = map(lambda movie: jsonify_movie_location(movie), movies)
 
    return jsonify({'movies': movies})

def fetch_movie(movie_id):
    """Return a JSON representation of a movie location shot in San Francisco.

    Arguments:
    - `movie_id`: the id of the movie to be retrieved.
    """
    movie = MovieLocation.query.filter(
        MovieLocation.id == movie_id).first()

    return jsonify_movie_location(movie)

def check_property_type(parameter, value, properties):
    """Checks if a parameter name is valid, raises an error if this is not the
        case.
        
        Arguments:
        - `parameter`: the parameter name.
        - `value`: the value of the parameter.
        - `properties`: the properties array of valid fields.
        """
    
    if parameter not in properties:
        raise_invalid_message(format(parameter))
    
    if value == "":
        raise_invalid_message(format(parameter) + ": \"\"")
    
    if parameter == 'id' or parameter == 'year':
        try:
            int(value)
        except:
            raise_invalid_message(format(parameter) + ":" + format(value))
    
    if parameter == 'longitude' or parameter == 'latitude':
        try:
            float(value)
        except:
            raise_invalid_message(format(parameter) + ":" + format(value))

def raise_invalid_message(error_message):
    """Raise an invalid exception indicating the internal error
        
       Arguments:
       - `error_message`: the message for the error
        """
    url = request.url
    api_index = url.index('/api/')
    url_suffix = urllib2.unquote(request.url[api_index:])
    raise InvalidUsage('Invalid: ' + error_message,
                       status_code=400,
                       payload={'links': [
                                          {'href': url_suffix,
                                          'rel': 'self'}]})    

def jsonify_movie_location(movie_location):
    """Takes a MovieLocation object and returns its JSON representation.
        
        Arguments:
        - `movie_location`: The MovieLocation object to jsonify.
        """
    
    fields = ['id', 'title', 'year', 'location', 'fun_fact',
              'production_company', 'distributor', 'director', 'writer',
              'actor_1', 'actor_2', 'actor_3', 'latitude', 'longitude',
              'links']
    
    json_movie = {}
    
    for field in fields:
        fieldValue = getattr(movie_location, field, None)
        if fieldValue is not None:
            json_movie[field] = fieldValue
    
    if 'links' in fields:
        json_movie['links'] = [
                               {'rel': 'self',
                               'href': '/api/v1/movies/' + str(movie_location.id)}
                               ]
    
    return json_movie

