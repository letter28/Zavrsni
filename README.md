# Zavrsni
My Final paper, in development phase.

The goal is a web application for graphical display of production data from a photo-voltaic system in front of Faculty of Engineering, in Rijeka, Croatia. The design of the app includes two Python scripts running at the same time, one retrieving the data from a local server on college and storing it into a SQL table; and the other for live display (5 min. interval) of that data. Long range goals are to analize the data, and make it available for download and further manipulation. Technologies used in this project: Python 3.7.0, MySQL 8.0, Dash(Flask based).

Currently:
- the data retrieval and storage work as intended
- the core dash app is working locally
- added tabs: 1) one for viewing the data live (done)
              2) the other for the table (done) and download option (in progress)  
- added a graph for viewing the AC and DC power output
- added a table with data pulled from the db
- added graphical represantation of available data
- added some styling (background color, text colors, centering)
- added graphical and textual representation of live data

The next steps in the project:
- add feature of pulling the data from the db requested by the user (range option)

