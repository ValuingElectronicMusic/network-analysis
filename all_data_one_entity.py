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
import outward_waves

time_delay = 2

def user_dicts(resourcelist):
    return {u.obj['id']:u.obj for u in resourcelist}


def get_data(req):
    '''Mostly copied from outward_waves.py'''
    collected = {}
    start_at = 0
    batch_length = 199
    mouthful = 199
    while batch_length > 198:
        count = 1
        while True:
            try:
                if req[-1].isdigit():
                    return gsd.client.get(req)
                else:
                    batch=user_dicts(gsd.client.get(req,
                                                    order='created_at', 
                                                    limit=mouthful,
                                                    offset=start_at))
                    collected.update(batch)
                    batch_length = len(batch)
                    start_at += mouthful
                    break
            except Exception as e:
                if str(e)[:3]=='404': # does not exist 
                    return None

                if str(e)[:3]=='500': # too much data for server
                    mouthful = mouthful / 2
                    if mouthful < 1: mouthful = 1

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


def track_data(track_id):
    td=get_data('/tracks/'+str(track_id))
    if td:
        return td.obj
    else:
        return False


def comment_data(comment_id):
    cd=get_data('/comments/'+str(comment_id))
    if cd:
        return cd.obj
    else:
        return False


def user_followings(user_id):
    return get_data('/users/'+str(user_id)+'/followings')


def user_followers(user_id):
    return get_data('/users/'+str(user_id)+'/followers')


def tracks_by_user(user_id):
    return get_data('/users/'+str(user_id)+'/tracks')


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


def related_data_one_user(curs,user):
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


def collect_user(curs,user):
    try:
        curs.execute('INSERT INTO ids_tried (id) VALUES(?)',(user,))
    except sqlite3.IntegrityError as ie:
        return False

    ud=user_data(user)
    if not ud: return False

    curs.execute('INSERT INTO sample (id) VALUES(?)',(user,))
    insert_into_table(curs,'users',ud)
    related_data_one_user(curs,user)

    return True


def collect_track(curs,track):
    try:
        curs.execute('INSERT INTO ids_tried (id) VALUES(?)',(track,))
    except sqlite3.IntegrityError as ie:
        return False

    td=track_data(track)
    if not td: return False
    curs.execute('INSERT INTO sample (id) VALUES(?)',(track,))
    insert_into_table(curs,'tracks',td)

    tu=user_data(td['user_id'])
    if tu: insert_into_table(curs,'users',tu)

    return True


def collect_comment(curs,comment):
    try:
        curs.execute('INSERT INTO ids_tried (id) VALUES(?)',(comment,))
    except sqlite3.IntegrityError as ie:
        return False

    cd=comment_data(comment)
    if not cd: return False
    curs.execute('INSERT INTO sample (id) VALUES(?)',(comment,))
    insert_into_table(curs,'comments',cd)

    cm=user_data(cd['user_id'])
    if cm: insert_into_table(curs,'users',cm)

    td=track_data(cd['track_id'])
    if td: insert_into_table(curs,'tracks',td)

    tu=user_data(td['user_id'])
    if tu: insert_into_table(curs,'users',tu)

    return True
