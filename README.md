network-analysis
=============

Code for exploring the value of electronic music via analysing 
network interactions on Soundcloud. Authors: annajordanous, 
daniel-allington Language: Python (2.7) Version 1.0

Originally based on code for analysing interactions on IFDB: see 
https://github.com/ValuingElectronicMusic/ifdb-analysis (Author: 
daniel-allington)

-----------------

NB to run this code, you need to be registered on SoundCloud as a 
developer and have a client id. 

This should be reasonably straightforward:
1. Register an account on Soundcloud.com (if you don't already have one).
2. Log into your Soundcloud account (if not already logged in).
3. At developers.soundcloud.com, navigate to 'Register a new app' 
   and follow the steps there
    (this is currently at http://soundcloud.com/you/apps/new)
4. You will be given a client_id once you have finished registering. 
    Edit clientSettingsDEMO.py to enter your client_id. 
5. Save clientSettingsDEMO.py as clientSettings.py

Sorry for any inconvenience. We introduced this authentication step in 
our code to prevent any malicious use of our code under our client id, to
overload the SoundCloud servers.

-------------

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
