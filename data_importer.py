#!/usr/bin/env python

"""
The loading script is executed after log_lat_convert.py when
all the movies are associated with a (longitude, latitude) pair
"""

# # Imports

import sys
import json
from app import models
from app import db
import optparse
import commands

def is_qualified(movie):

    """ Check if the movie is with enough info for entering the db 
    """

    if 'locations' not in movie or 'title' not in movie \
        or 'release_year' not in movie or 'latitude' not in movie \
        or 'longitude' not in movie:
            return False;
    return True;   

def dump_to_db(filePath)

    """Reads a JSON file created by log_lat_converter.py, containing 
       movie locations along with the longtitude and latitude  
       and imports them into the application database.
    """

    # Read JSON file
    print "Reading JSON file"
    fileIn = open(filePath, 'r')
    movies = json.load(fileIn)
    fileIn.close()

    print "Parsing Movie objects"
    for movie in movies:

        # simple filter for movies lack of interesting information
        if not is_qualified(movie):
            continue

        # Extract fields
        location = movie['locations'].strip()
        title = movie['title'].strip()
        year = int(movie['release_year'].strip())
        latitude = movie['latitude']
        longitude = movie['longitude']

        fun_fact = movie['fun_facts'].strip() if 'fun_facts' in movie else ""
        production_company = movie['production_company'].strip() if 'production_company' in movie else ""
        distributor = movie['distributor'].strip() if 'distributor' in movie else ""
        director = movie['director'].strip() if 'director' in movie else ""
        writer = movie['writer'].strip() if 'writer' in movie else ""
        actor_1 = movie['actor_1'].strip() if 'actor_1' in movie else ""
        actor_2 = movie['actor_2'].strip() if 'actor_2' in movie else ""
        actor_3 = movie['actor_3'].strip() if 'actor_3' in movie else ""

        # Create model object
        movieObj = models.MovieLocation(title=title,
                                        year=year,
                                        location=location,
                                        fun_fact=fun_fact,
                                        production_company=production_company,
                                        distributor=distributor,
                                        director=director,
                                        writer=writer,
                                        actor_1=actor_1,
                                        actor_2=actor_2,
                                        actor_3=actor_3,
                                        latitude=latitude,
                                        longitude=longitude)

        # Add to transaction
        db.session.add(movieObj)

    # Commit transaction
    db.session.commit()
    print "Script finished successfully"

def main():

    '''
    INPUT FORMAT
    input_file   : the path of the input file.
    USAGE EXAMPLE
    python log_lat_converter.py -i data_with_lat_log.txt 
    '''

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input_path", dest="input_path",
                      help="the input path")

    (options, args) = parser.parse_args()
    dump_to_db(options.input_path)

if __name__ == "__main__":
    main()

