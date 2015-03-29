# uber-code-challenge

This project presents a solution to the SF Movies coding challenge.

SF Movies: Create a service that shows on a map where movies have been filmed in San Francisco. The user should be able to filter the view using autocompletion search.

MVC Structure:
viewer.py: view layer
controller.py: control layer
models.py: model layer

process:
1. execute data_importer.py and log_lat_converter.py for pre-processing data with longtitude and latitude information 
   The data will be saved in the home_location in the postgres

2. run python runp.py to start the service


