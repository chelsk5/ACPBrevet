# ACP Brevet Control Times Calculator

The ACP Calculator is a tool designed to calculate open and close times for ACP-sanctioned brevets based on the rules outlined by the Audax Club Parisien (ACP).

## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.   

This essentially replaces the calculator here (https://rusa.org/octime_acp.html). 

## Features

* Calculate open and close times for control points in brevet events.

* Each time a distance is filled in, the corresponding open and close times should be filled in.   

* If 'Submit' button is pressed, times and distances currently in table will be stored in MongoDB database.

* If 'Display' button is pressed, all times and distances input and submitted will be displayed in a new page.

* If no controle times are entered in the table, an error message will appear on the page.

* If times are submitted successfully, a success message will appear on the page.

* Supports brevet distances of 200, 300, 400, 600, and 1000 kilometers.

* Distances 20% or less over total brevet have open and close times equal to that of the brevet distance.

* Entering distances over 20% more than total brevet distance results in an error message appearing.

* Only numeric input is accepted as input for distances.

* Expose what is stored in MongoDB using the following three basic APIs:
    * `http://<host:port>/listAll` should return all open and close times in the database
    * `http://<host:port>/listOpenOnly` should return open times only
    * `http://<host:port>/listCloseOnly` should return close times only

* There are two different representations: one in csv and one in json. JSON is the default representation. 
    * `http://<host:port>/listAll/csv` should return all open and close times in CSV format
    * `http://<host:port>/listOpenOnly/csv` should return open times only in CSV format
    * `http://<host:port>/listCloseOnly/csv` should return close times only in CSV format

    * `http://<host:port>/listAll/json` should return all open and close times in JSON format
    * `http://<host:port>/listOpenOnly/json` should return open times only in JSON format
    * `http://<host:port>/listCloseOnly/json` should return close times only in JSON format

* To get top "k" open and close times, see below.

    * `http://<host:port>/listOpenOnly/csv?top=3` should return top 3 open times only (in ascending order) in CSV format 
    * `http://<host:port>/listOpenOnly/json?top=5` should return top 5 open times only (in ascending order) in JSON format
    * `http://<host:port>/listCloseOnly/csv?top=6` should return top 5 close times only (in ascending order) in CSV format
    * `http://<host:port>/listCloseOnly/json?top=4` should return top 4 close times only (in ascending order) in JSON format

## Usage

* Select brevet distance from menu.

* Specify start date and time.

* Enter the desired control distance in kilometer or miles.

* Save times in database using 'Submit' button.

* View saved times using 'Display' button.

## How to Use

* Have Docker downloaded and running

* Open 'DockerRestAPI' directory

* add credentials.ini to directory

* run 'docker-compose build' followed by 'docker-compose up' from the command line

* go to http://localhost:9320/ to input times to database

* to view inputs using consumer program, go to http://localhost:9420/

## Acknowledgements

* Credits to Michal Young for the initial version of this code.

## Author

* Chelsea Kendrick

* ckendri5@uoregon.edu

