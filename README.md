# uber-code-challenge

This project presents a solution to the SF Movies coding challenge.

SF Movies: Create a service that shows on a map where movies have been filmed in San Francisco. The user should be able to filter the view using autocompletion search.

Architecture:

The solution mainly focuses on back-end and considers the functions claimed by the MVC structure. The UI inferface isprovided by the existing libraries. Below is the brief introduction of each scripts where their names have been highlighted by their functions.  

Online part:

app/viewer.py: view layer, for html send and recv, render web page, call functions provided by the controller layer

app/controller.py: control layer, for process data from the model layer and return back to the viewer layer

app/models.py: model layer, for return the data from db

app/error_displayer: for managing the internal error

offline part:

log_lat_converter.py: given the json file downloaded from the website, call google api to get the longtitude and latitude

data_importer.py: give the json file with long/lat, dump them into the database 

Future Improvement:

Online parts
1) need logger.py to capture all the behaviors of users for future analysis. These data will be used for data mining projects. 

2) As a project used by many users, we need to load balancer in front of web servers.

3) The data provided by the database need to be cached properly, in redis/memcached/hbase. 

Offline part:

1) Need a scanner to periodically monitor the change of data source. 

2) Need a checker to guarantee the data quality of incoming data.

Test part:

1) for test_controller.py, it depends on the data from real db for testing, which is not expected in the
actual development. We should rely on some mock interface.

2) Due to the time limit, the coverage of test cases may not be enough

How to launch the service:

1. execute data_importer.py and log_lat_converter.py for pre-processing data with longtitude and latitude information 
   The data will be saved in the home_location in the postgres

2. run python runp.py to start the service

