# Zavrsni
My Final paper, in development phase.

The goal is a web application for graphical display of production data from a photo-voltaic system in front of Faculty of Engineering, in Rijeka, Croatia. The design of the app includes two Python scripts running at the same time, one retrieving the data from a local server on college and storing it into a SQL table; and the other for live display (5 min. interval) of that data. Long range goals are to analize the data, and make it available for download and further manipulation. Technologies used in this project: Python 3.6, MySQL 8.008, pandas, requests, Dash(Flask based).

Currently:
- the data retrieval and storage work as intended

The next steps in the project:
- to set up the core app locally
- graphical and textual representation of available data
- graphical and textual representation of live data
- add tabs: 1) one for viewing of data live
            2) the other containing a table with data pulled from the db -> requested by the user (range option)
