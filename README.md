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
    Edit client_settingsDEMO.py to enter your client_id. 
5. Save client_settingsDEMO.py as client_settings.py

Sorry for any inconvenience. We introduced this authentication step in 
our code to prevent any malicious use of our code under our client id, to
overload the SoundCloud servers.

-------------

This code has been run and tested in Python 2.7
To collect SoundCloud data, use get_new_snowball_sample().
It has the following parameters and default values:
* sample_size=500, 
* desired_seed_users=set(), 
* batch_size=100, 
* pause_between_batches=10, 
* db_to_add_data_from = None

This function generates a new sample of users (set to the 
specified or default sample size), also generating
data on those users' tracks and how the users interact 
with other users on SoundCloud.

Example of running this from a Python 2.7 prompt ($)
$ import get_soundcloud_data as gsc 
$ gsc.get_new_snowball_sample(sample_size=10, 
    desired_seed_users={63287951},
    batch_size=2, pause_between_batches=2)  

(Other param not specified, default value will be used)

Data will be stored in a local 'sqdb_FINAL.sqlite' DB file

---------------

Future work.

---------------

THE FOLLOWING CODE IS SO FAR ONLY FUNCTIONAL FOR SMALL SAMPLES:
(tested successfully up to 500 users) 
* To analyse pre-collected soundcloud data (in sqdb.sqlite DB file), 
generating 3 separate measures of influence and graph diagrams:

$ import scdb_sna as scna

$ scna.demonstrate()

Measures of influence will be output to the screen and graphs
will be stored locally as .png files
