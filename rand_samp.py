# Do random sample:
#  - Begin with sample size
#  - Pick a random user ID
#  - Check that it's not in the database
#  - Call the function that gets all the data we need about a user
#  - Save everything
#  - Repeat until sample size reached

import sqlite3
import time
import random
import add_data as ad
import all_data_one_person as adop


db_path = 'rand_samp'


def time_stamp():
    return time.strftime('%Y%m%d_%H%M')


def connect(db_name):
    return sqlite3.connect(db_path+'/'+db_name+'.sqlite')


def create_tables(curs):
    for tabl in ['users','tracks','comments','x_follows_y','sample']:
        ad.create_table(curs,tabl)


Slackk = 202195
Sephirot = 81070
Sculpture = 261433 # Soundcloud website is 'tapebox'
Ms_Skyrym = 15899888
FAS = 55078931

#   As of 7 July 2014, there are nearly 103380000 SoundCloud accounts

def collect(sample_size=1,db=None):
    
    start_time=time_stamp()

    if db:
        conn=connect(db)
        curs=conn.cursor()
    else:
        conn=connect('rand_samp_'+start_time)
        curs=conn.cursor()
        create_tables(curs)

    collected, non_ids = 0,0

    while collected < sample_size:
        try_id = random.randint(0,104000000)
        print 'Trying '+str(try_id)
        if adop.collect(curs,try_id): 
            collected += 1
        else: 
            non_ids += 1
        conn.commit()

    return collected, non_ids, start_time, time_stamp()
