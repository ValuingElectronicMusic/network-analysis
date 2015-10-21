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
import all_data_one_entity as adoe


db_dirpath = 'rand_samp'
backup_dirpath = os.path.join('rand_samp','backup')
max_batch = 500
batches_before_backup = 100


collect_funcs = {'users':adoe.collect_user,
                 'tracks':adoe.collect_track,
                 'comments':adoe.collect_comment}

maxnums = {'users':182000000,
           'tracks':230000000,
           'comments':260000000}

#   As of 7 July 2014, there've been nearly 103380000 SoundCloud accounts
#   As of 28 July 2014, there've been between 160500000 and 160600000 tracks
#   As of 28 July 2014, there've been between 194000000 and 195000000 comments

#   As of 21 October 2015, there are somewhere approaching 182000000 accounts

def time_stamp():
    return time.strftime('%Y%m%d_%H%M')


def create_tables(curs):
    for tabl in ['users','tracks','comments','x_follows_y',
                 'ids_tried','track_ids_tried','comment_ids_tried','sample']:
        ad.create_table(curs,tabl)


def collect_batch(curs,batch_size,maxnum,collect_func):
    collected, non_ids = 0,0
    while collected < batch_size:
        try_id = random.randint(0,maxnum)
        if collect_func(curs,try_id): 
            collected += 1
        else: 
            non_ids += 1
    return collected, non_ids


def collect(sample_size=1,db_path=None,to_sample='users'):
    
    start_time=time_stamp()

    if db_path:
        db_name=os.path.split(db_path)[1]
        conn=sqlite3.connect(db_path)
        curs=conn.cursor()
    else:
        db_name='{}_rand_samp_{}'.format(to_sample,start_time)
        db_path=os.path.join(db_dirpath,db_name+'.sqlite')
        conn=sqlite3.connect(db_path)
        curs=conn.cursor()
        create_tables(curs)

    db_dir = os.path.split(db_path)[0]
    db_backup_dir = os.path.join(db_dir,'db_backup')
    if not os.path.exists(db_backup_dir):
        os.makedirs(db_backup_dir)

    non_ids = 0
    curs.execute('SELECT id FROM sample')
    collected = len(curs.fetchall())
    batches = 0

    while collected < sample_size:
        start=time.time()
        uncollected = sample_size - collected
        batch_size = (uncollected if uncollected <= max_batch else max_batch)
        collection=collect_batch(curs,batch_size,
                                 maxnums[to_sample],
                                 collect_funcs[to_sample])
        conn.commit()
        collected += collection[0]
        non_ids += collection[1]
        batches += 1
        print '{} collected.'.format(collected)
        print ('Time elapsed for '
               'this batch: {}'.format(int(time.time()-start)))
        if batches >= batches_before_backup or collected >= sample_size:
            print 'Backing up...'
            shutil.copyfile(db_path,
                            os.path.join(db_backup_dir,
                                         db_name+'_back_'
                                         +time_stamp()+'.sqlite'))
            batches = 0
        print ("Pausing 20s. If you've been planning to interrupt, "
               "now's your chance.")
        time.sleep(20)
        print 'Stopped pausing now.'

    return collected, non_ids, start_time, time_stamp()


def seek_limit(resource_func,start_at,stop_at=0):
    '''resource_func should be adoe.user_data, adoe.track_data, or
    adoe.comment_data'''
    
    current_num = start_at
    while current_num > stop_at:
        a=resource_func(current_num)
        if a:
            print 'A very palpable hit!'
            return current_num
        else:
            current_num -= random.randint(0,100)

    return None
