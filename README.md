# uber-code-challenge

This project presents a solution to the SF Movies coding challenge.

SF Movies: Create a service that shows on a map where movies have been filmed in San Francisco. The user should be able to filter the view using autocompletion search.

MVC Structure:

Online part:

app/viewer.py: view layer, for html send and recv, render web page, call functions provided by the controller layer

app/controller.py: control layer, for process data from the model layer and return back to the viewer layer

app/models.py: model layer, for return the data from db

app/error_displayer: for managing the internal error

offline part:

log_lat_converter.py: given the json file downloaded from the website, call google api to get the longtitude and latitude

data_importer.py: give the json file with long/lat, dump them into the database 

How to launch the service:

1. execute data_importer.py and log_lat_converter.py for pre-processing data with longtitude and latitude information 
   The data will be saved in the home_location in the postgres

2. run python runp.py to start the service

Future Improvement:

app/logger.py: need to capture all the behaviors of users for future analysis

tests/test_controller.py: depend on the data from real db, should rely on some mock interface

tests: the coverage of test cases need to increase


