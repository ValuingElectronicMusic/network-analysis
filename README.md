network-analysis
=============

Code for exploring the value of electronic music via analysing 
network interactions on Soundcloud. Authors: annajordanous, 
daniel-allington Language: Python (2.7) Version 1.0

Originally based on code for analysing interactions on IFDB: see 
https://github.com/ValuingElectronicMusic/ifdb-analysis (Author: 
daniel-allington)

-----------------

To run the code from a Python 2.7 prompt ($)

* To collect data from soundcloud (e.g. to collect 100 users) and 
save this data locally in an SQLite database: 

$ import getSoundCloudData as gsc 

$ gsc.main(100)

Data will be stored in a local 'sqdb.sqlite' DB file

* To analyse pre-collected soundcloud data (in sqdb.sqlite DB file), 
generating 3 separate measures of influence and graph diagrams:

$ import scdb_sna as scna

$ scna.demonstrate()

Measures of influence will be output to the screen and graphs
will be stored locally as .png files
