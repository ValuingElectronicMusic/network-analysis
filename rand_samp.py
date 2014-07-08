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
import shutil
import os.path
import add_data as ad
import all_data_one_person as adop


db_dirpath = 'rand_samp'
backup_dirpath = 'rand_samp/backup'
max_batch = 1000


def time_stamp():
    return time.strftime('%Y%m%d_%H%M')


def create_tables(curs):
    for tabl in ['users','tracks','comments','x_follows_y','sample']:
        ad.create_table(curs,tabl)


def collect_batch(curs,batch_size):
    collected, non_ids = 0,0
    while collected < batch_size:
        try_id = random.randint(0,104000000)
        print 'Trying '+str(try_id)
        if adop.collect(curs,try_id): 
            collected += 1
        else: 
            non_ids += 1
    return collected, non_ids


#   As of 7 July 2014, there are nearly 103380000 SoundCloud accounts

def collect(sample_size=1,db_name=None):
    
    start_time=time_stamp()

    if db_name:
        conn=sqlite3.connect(os.path.join(db_dirpath,db_name+'.sqlite'))
        curs=conn.cursor()
    else:
        db_name='rand_samp_'+start_time
        conn=sqlite3.connect(os.path.join(db_dirpath,db_name+'.sqlite'))
        curs=conn.cursor()
        create_tables(curs)

    collected, non_ids = 0,0

    while collected < sample_size:
        uncollected = sample_size - collected
        batch_size = (uncollected if uncollected <= max_batch else max_batch)
        collection=collect_batch(curs,batch_size)
        conn.commit()
        collected += collection[0]
        non_ids += collection[1]
        print '{} collected.'.format(collected)
        print 'Backing up...'
        shutil.copyfile(os.path.join(db_dirpath,
                                     db_name+'.sqlite'),
                        os.path.join(backup_dirpath,
                                     db_name+'_back_'+time_stamp()+'.sqlite'))
        print "Pausing 3 minutes. If you've been planning to interrupt, now's your chance."
        time.sleep(180)

    return collected, non_ids, start_time, time_stamp()
