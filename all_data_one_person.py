# Get all the data we need for one person:
#  - Basic user info
#  - All his/her followers
#  - All those he/she follows
#  - All comments he/she has made
#  - All tracks he/she has uploaded
#  - All comments made on all those tracks

# Code is mostly cribbed from comment_interactions.py

import add_data as ad
import get_soundcloud_data as gsd
import genre_relationships as gr
import sqlite3
import collections
import time

time_delay = 2
max_attempts = 100
n = 10


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
                if req[-1].isdigit():
                    return gsd.client.get(req)
                else:
                    batch=user_dicts(gsd.client.get(req,
                                                    order='created_at', 
                                                    limit=199,
                                                    offset=start_at))
                    collected.update(batch)
                    batch_length = len(batch)
                    start_at += 199
                    break
            except Exception as e:
                if str(e)[:3]=='404': 
                    return None

                warning = ('ERROR in client.get() - problem connecting to '
                           'SoundCloud API, error '+str(e)+' for '
                           'request '+req+'. Trying again... '
                           'attempt '+str(count))
                print warning
                time.sleep(time_delay * count)
                count += 1
    return collected


def user_data(user_id):
    ud=get_data('/users/'+str(user_id))
    if ud:
        return ud.obj
    else:
        return False


def user_followings(user_id):
    return get_data('/users/'+str(user_id)+'/followings')


def user_followers(user_id):
    return get_data('/users/'+str(user_id)+'/followers')


def tracks_by_user(user_id):
    return get_data('/users/'+str(user_id)+'/tracks')


def track_data(track_id):
    return gsd.client.get('/tracks/'+str(track_id)).obj


def comments_on_track(track_id):
    return get_data('/tracks/'+str(track_id)+'/comments')


def comments_by_user(user_id):
    return get_data('/users/'+str(user_id)+'/comments')


def insert_into_table(curs,table,data):

    att_str=ad.att_string(ad.tables[table])
    att_lst=ad.att_list(att_str)
    sql=('INSERT INTO {} ({}) '
         'VALUES({})'.format(table,att_str,('?, '*len(att_lst))[:-2]))
    try: 
        data_to_add=[(data[key] if key in data.keys() else None) 
                     for key in att_lst]
        curs.execute(sql,data_to_add)
    except sqlite3.IntegrityError as ie:
        pass


def collect_for_user(curs,user):
    followers=user_followers(user)
    for follower in followers:
        follr=followers[follower]
        insert_into_table(curs,'users',follr)
        insert_into_table(curs,'x_follows_y',
                          {'follower':follr['id'],
                           'followed':user})

    followeds=user_followings(user)
    for followed in followeds:
        folld=followeds[followed]
        insert_into_table(curs,'users',folld)
        insert_into_table(curs,'x_follows_y',
                          {'follower':user,
                           'followed':folld['id']})

    tracks=tracks_by_user(user)
    for track in tracks:
        insert_into_table(curs,'tracks',tracks[track])
        comments_on = comments_on_track(track)
        for comment in comments_on:
            com=comments_on[comment]
            insert_into_table(curs,'comments',com)
            insert_into_table(curs,'users',
                              user_data(com['user_id']))

    comments_by=comments_by_user(user)
    for comment in comments_by:
        com=comments_by[comment]
        insert_into_table(curs,'comments',com)
        track=track_data(com['track_id'])
        insert_into_table(curs,'tracks',track)
        insert_into_table(curs,'users',
                          user_data(track['user_id']))


def collect(curs,user):
    try:
        curs.execute('INSERT INTO sample (id) VALUES(?)',(user,))
    except sqlite3.IntegrityError as ie:
        return False

    ud=user_data(user)
    if not ud: return False

    insert_into_table(curs,'users',ud)
    collect_for_user(curs,user)

    return True


