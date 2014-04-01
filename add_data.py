'''
Created on Apr 1, 2014

@author: daniel-allington
'''

import sqlite3
import string


# Strings used for creating tables. Note that I've removed the primary
# keys because they don't seem to work properly in SQLite and in most
# cases the result will be a smaller table.

dummy_table_creator='id INTEGER, user_id INTEGER, title TEXT'

tracks_table_creator='''id INTEGER, user_id INTEGER, title TEXT,
permalink_url TEXT,  track_type TEXT, state TEXT, created_at TEXT,
original_format TEXT, description TEXT, sharing TEXT,
genre TEXT, duration INTEGER, key_signature TEXT, bpm INTEGER,
license TEXT, label_name TEXT,
favoritings_count INTEGER,
streamable TEXT, stream_url TEXT,
downloadable TEXT, download_count INTEGER,
commentable TEXT,
purchase_url TEXT, artwork_url TEXT, video_url TEXT, embeddable_by TEXT,
release TEXT, release_month INTEGER, release_day INTEGER, release_year INTEGER,
tag_list TEXT'''

users_table_creator='''id INTEGER, username TEXT, 
permalink_url TEXT, full_name TEXT, description TEXT,  
city TEXT, country TEXT, 
track_count INTEGER, playlist_count INTEGER, 
followers_count INTEGER, followings_count INTEGER, 
public_favorites_count INTEGER'''

x_follows_y_table_creator='follower INTEGER, followed INTEGER'

groups_table_creator='user_id INTEGER, group_id INTEGER'

favourites_table_creator='user INTEGER, track INTEGER'

comments_table_creator='''id INTEGER,
body TEXT, user_id INTEGER, track_id INTEGER, 
timestamp INTEGER, created_at TEXT)'''


# Generalised function for creating each of the tables we need, using
# the above strings

def create_table(cursor,table,table_creator):
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table))
    cursor.execute('CREATE TABLE IF NOT '
                   'EXISTS {}({})'.format(table,table_creator))


# Functions for turning table-creating strings (above) into lists of
# attributes

def att_string(str):
    return str.translate(None,string.ascii_uppercase)


def att_list(att_str):
    return [att.strip() for att in att_str.split(',')]


# Function for getting data out of SoundCloud object (null if missing)

def obj_atts_list(obj, att_list):
    l = []
    for att in att_list:
        try:
            l.append(getattr(obj,att))
        except AttributeError:
            l.append('NULL')
    return l


# Generalised function for putting data into tables created
# above, based on what's currently in getSoundCloudData.py

def insert_data_loop(cursor, table, data, att_list):
    sql='INSERT INTO {} VALUES({})'.format(table,('?, '*len(att_list))[:-2])
    for datum in data:
        try:
            vals=tuple(obj_atts_list(datum,att_list))
            cursor.execute(sql,vals)
        except Exception as e:
            print('Error adding {} to '
                  '{}: {} {}'.format(datum.id,table,e.message,e.args))


# (Probably) more efficient version of the above. We hopefully won't
# need the exception handling once we've got it working properly.

def insert_data(cursor, table, data, att_list):
    sql='INSERT INTO {} VALUES({})'.format(table,('?, '*len(att_list))[:-2])
    vals = [tuple(obj_atts_list(d,att_list)) for d in data]
    cursor.executemany(sql,vals)


# Unit tests follow. N.B. if this module is imported by e.g.
# getSoundCloudData.py, test1() and test2() provide a model for how
# the above functions can be called.

class placeholder():
    pass


def dummy_data():
    ph1 = placeholder()
    ph1.id = 12345
    ph2 = placeholder()
    ph2.id = 67890
    ph2.user_id = 11102
    return [ph1,ph2]


def test1():
    test_data = dummy_data()
    connection = sqlite3.connect('test1.sqlite')
    cursor = connection.cursor()
    create_table(cursor,'dummy',dummy_table_creator)
    insert_data(cursor,'dummy',test_data,
                att_list(att_string(dummy_table_creator)))
    connection.commit()


def test2():
    test_data = dummy_data()
    connection = sqlite3.connect('test2.sqlite')
    cursor = connection.cursor()
    create_table(cursor,'tracks',tracks_table_creator)
    insert_data(cursor,'tracks',test_data,
                att_list(att_string(tracks_table_creator)))
    connection.commit()
