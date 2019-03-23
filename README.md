# Zavrsni
My Final paper, in development phase.

The goal is a web application for graphical display of production data from a photo-voltaic system in front of Faculty of Engineering, in Rijeka, Croatia. The design of the app includes two Python scripts running at the same time, retrieving the data from a local server on college and storing it into a SQL table; the Dash app itself is served on heroku and runs in a separate process. Long range goals are to analize the data, and make it available for download and further manipulation. Technologies used in this project: Python 3.7.0, MySQL 8.0, Dash(Flask based).

I will soon update this readme with instructions for the installation.

App is available at: https://fne-test-app.herokuapp.com

Currently:
- the data retrieval and storage work as intended
- the core dash app is working locally
- added tabs: 1) one for viewing the data live (done)
              2) the other for the table (done) and download option (done)  
- added a graph for viewing the AC and DC power output
- added a table with data pulled from the db
- added graphical represantation of available data
- added some styling (background color, text colors, centering)
- added graphical and textual representation of live data
- added date picker range for both graph and table data
- added data download link
- added live meteorological data
- deployed the app on heroku

The next steps in the project:
- unknown
