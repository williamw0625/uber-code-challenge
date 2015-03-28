#!/usr/bin/env python

# Reads a JSON file downloaded from 
# https://data.sfgov.org/Culture-and-Recreation/Film-Locations-in-San-Francisco/yitu-d5am? 
# where movie locations are represented by address.
# Convert them into the representation of longitude and latitude using Google Map API; 

import sys
import json
import urllib2
from time import sleep
from config import SERVER_KEY
from config import GOOGLE_MAP_URL
import optparse
import commands

def convert(inputFilePath, outputFilePath):

  # Read JSON file
  print "Reading JSON file"
  fileIn = open(inputFilePath, 'r')
  movies = json.load(fileIn)
  fileIn.close()

  # Perform geocoding
  print "Performing requests"
  for movie in movies:
    print "Entry: %d" % counter
    if 'locations' not in movie.keys():
      continue

    encodedLocation = urllib2.quote(movie['locations'].encode("utf8"))
    requestUrl = GOOGLE_MAP_URL + "json?address=" + encodedLocation + ",+San+Francisco,+CA"
    print requestUrl
    jsonResponse = json.load(urllib2.urlopen(requestUrl))

    if len(jsonResponse['results']) > 0:
      coordinates = jsonResponse['results'][0]['geometry']['location']
      movie['latitude'] = coordinates['lat']
      movie['longitude'] = coordinates['lng']
      print movie

    sleep(0.1)

  # Write augmented JSON file
  print "Writing output"
  fileOut = open(outputFilePath, 'w')
  json.dump(movies, fileOut)
  fileOut.close()
  print "Output written to: " + outputFilePath

  print "Script exited successfully"

def main():

  '''
  INPUT FORMAT
  input_file   : the path of the input file.

  OUPUT FORMAT:
  output_file : the path of the output file

  USAGE EXAMPLE
  python log_lat_converter.py -i data_without_lat_log.txt -o data_with_lat_log.txt 
  '''

  parser = optparse.OptionParser()
  parser.add_option("-i", "--input_path", dest="input_path",
                    help="the input path")
  parser.add_option("-o", "--output_path", dest="output_path",
                    help="the output path")

  (options, args) = parser.parse_args()
  convert(options.input_path, options.output_path)

if __name__ == "__main__":
  main()

