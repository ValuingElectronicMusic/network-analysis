# The idea of this is to get some data that can be used in a nice
# animated visualisation of people commenting on each other's
# tracks. It starts with a seed user, gets all of his/her comments,
# finds the n users whose tracks he/she commented on most frequently,
# gets all their tracks and all comments on them, then gets all the
# seed user's tracks and all the comments on them, finds the n users
# who most frequently commented on his/her tracks, and gets all their tracks
# and all comments on them.

# At the moment, the point is just to make sure that there's something
# worth looking at in the visualisations. But we can also potentially
# use this for analysis of conversations - and for constructing a
# network a la forward_waves.py. For what it's worth, I think it may
# make most sense to use this approach backwards (i.e. from a user to
# the users who commented on his/her tracks) as we can't get hold of all
# comments by a very prolific commenter.

import add_data as ad
import get_soundcloud_data as gsd
import genre_relationships as gr
import sqlite3
import time
import collections

db_path = 'comment_interactions'
time_delay = 2
max_attempts = 100
n = 10


def time_stamp():
    return time.strftime('%Y%m%d_%H%M')


def user_dicts(resourcelist):
    return {u.obj['id']:u.obj for u in resourcelist}


def get_data(req):
    '''Mostly copied from forward_waves.py'''
    collected = {}
    start_at = 0
    batch_length = 199
    while batch_length > 198:
        count = 1
        while True:
            try:
                batch=user_dicts(gsd.client.get(req,
                                                order='created_at', 
                                                limit=199,
                                                offset=start_at))
                collected.update(batch)
                batch_length = len(batch)
                start_at += 199
                break
            except Exception as e:
                warning = ('ERROR in client.get() - problem connecting to '
                           'SoundCloud API, error '+str(e)+' for '
                           'request '+req+'. Trying again... '
                           'attempt '+str(count))
                print warning
                time.sleep(time_delay * count)
                count += 1
    return collected


def user_data(user_id):
    return gsd.client.get('/users/'+str(user_id)).obj


def tracks_by_user(user_id):
    return get_data('/users/'+str(user_id)+'/tracks')


def comments_on_track(track_id):
    return get_data('/tracks/'+str(track_id)+'/comments')


def comments_by_user(user_id):
    return get_data('/users/'+str(user_id)+'/comments')


def find_author(track_id):
    count = 1
    while True:
        try:
            return gsd.client.get('/tracks/'+str(track_id)).obj['user_id']
        except Exception as e:
            warning = ('ERROR in client.get() - problem connecting to '
                       'SoundCloud API, error '+str(e)+' for '
                       'request '+req+'. Trying again... '
                       'attempt '+str(count))
            print warning
            time.sleep(time_delay * count)
            count += 1


def most_commented_on_by(user_id):
    coms = comments_by_user(user_id)
    com_ons = [find_author(coms[c]['track_id']) for c in coms]
    return [c[0] for c in collections.Counter(com_ons).most_common(n+1)]


def connect(db_name):
    return sqlite3.connect(db_path+'/'+db_name+'.sqlite')


def create_tables(curs):
    for tabl in ['users','tracks','comments']:
        ad.create_table(curs,tabl)


def insert_into_table(curs,table,data):
    att_str=ad.att_string(ad.tables[table])
    att_lst=ad.att_list(att_str)
    sql=('INSERT INTO {} ({}) '
         'VALUES({})'.format(table,att_str,('?, '*len(att_lst))[:-2]))
    curs.execute(sql,[(data[key] if key in data.keys() else None) 
                      for key in att_lst])
    

#        try:
#            curs.execute(sql,datum)
#        except sqlite3.IntegrityError as ie:
#            pass


def collect_for_user(user,curs):
    ud=user_data(user)
    insert_into_table(curs,'users',ud)
    tracks=tracks_by_user(user)
    commenters=[]
    for track in tracks:
        insert_into_table(curs,'tracks',tracks[track])
        comments = comments_on_track(track)
        for comment in comments:
            insert_into_table(curs,'comments',comments[comment])
            commenters.append(comments[comment]['user_id'])
    return commenters


Slackk = 202195
Sephirot = 81070
Sculpture = 261433 # Soundcloud website is 'tapebox'
Ms_Skyrym = 15899888
FAS = 55078931


def collect(seed):
    conn=connect('seed_'+str(seed)+'_'+time_stamp())
    curs=conn.cursor()
    create_tables(curs)
    commenters=collect_for_user(seed,curs)
    conn.commit()
    to_collect=collections.Counter(commenters).most_common(n+1)
    cs = [c[0] for c in to_collect]
    cs.extend(most_commented_on_by(seed))
    cs = [c for c in cs if c!=seed]
    for commenter in cs:
        collect_for_user(commenter,curs)
        conn.commit()
