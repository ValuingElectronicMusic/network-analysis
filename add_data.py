'''
Created on Apr 1, 2014

@author: daniel-allington
'''

import sqlite3
import re


# Strings used for creating tables. Note that I've removed the primary
# keys because they didn't seem to work properly and I didn't have time
# to fix them. But with the code packaged up in single functions as below
# I'm hopeful it will only need to be fixed once!

dummy_table_creator='id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT'

tracks_table_creator='''id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,
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

users_table_creator='''id INTEGER PRIMARY KEY, username TEXT, 
permalink_url TEXT, full_name TEXT, description TEXT,  
city TEXT, country TEXT, 
track_count INTEGER, playlist_count INTEGER, 
followers_count INTEGER, followings_count INTEGER, 
public_favorites_count INTEGER'''

x_follows_y_table_creator='''follower INTEGER, followed INTEGER, 
PRIMARY KEY (follower, followed)'''

groups_table_creator='''user_id INTEGER, group_id INTEGER, 
PRIMARY KEY (user_id, group_id)'''

favourites_table_creator='''user INTEGER, track INTEGER, 
PRIMARY KEY (user, track)'''

comments_table_creator='''id INTEGER PRIMARY KEY,
body TEXT, user_id INTEGER, track_id INTEGER, 
timestamp INTEGER, created_at TEXT'''


# Generalised function for creating each of the tables we need, using
# the above strings

def create_table(cursor,table,table_creator):
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table))
    cursor.execute('CREATE TABLE IF NOT '
                   'EXISTS {}({})'.format(table,table_creator))


# Functions for turning table-creating strings (above) into strings
# containing only column names

def att_string(str):
    return re.sub(r'\n|[A-Z]|\(.*?\)','',str).strip(', ')


# Function for turning string containing column names into list

def att_list(att_str):
    return [att.strip() for att in att_str.split(',')]


# Function for getting data out of SoundCloud object (null if missing)

def obj_atts_list(obj, att_lst):
    l = []
    for att in att_lst:
        try:
            l.append(getattr(obj,att))
        except AttributeError:
            l.append('NULL')
    return l


# Generalised function for putting data into tables created
# above, based on what's currently in getSoundCloudData.py

def insert_data_loop(cursor, table, data, att_str, att_lst):
    sql='INSERT INTO {} ({}) VALUES({})'.format(table,att_str,('?, '*len(att_lst))[:-2])
    for datum in data:
        try:
            vals=tuple(obj_atts_list(datum,att_lst))
            cursor.execute(sql,vals)
        except Exception as e:
            print('Error adding {} to '
                  '{}: {} {}'.format(datum.id,table,e.message,e.args))


# (Probably) more efficient version of the above. We hopefully won't
# need the exception handling once we've got it working properly.

def insert_data(cursor, table, data, att_str, att_lst):
    sql='INSERT INTO {} ({}) VALUES({})'.format(table,att_str,('?, '*len(att_lst))[:-2])
    vals = [tuple(obj_atts_list(d,att_lst)) for d in data]
    cursor.executemany(sql,vals)


# Unit tests follow. test1(), test2(), and test3() will create a
# database with three tables, two of which will contain null values
# where the objects from which the data was drawn lacked expected
# attributes. N.B. if this module is imported by e.g.
# getSoundCloudData.py, these functions provide a model for how the
# above functions can be called.

class placeholder():
    pass


def dummy_data1():
    ph1 = placeholder()
    ph1.id = 12345
    ph2 = placeholder()
    ph2.id = 67890
    ph2.user_id = 11102
    return [ph1,ph2]


def dummy_data2():
    ph1 = placeholder()
    ph1.follower = 12345
    ph1.followed = 67890
    ph2 = placeholder()
    ph2.follower = 67890
    ph2.followed = 12345
    return [ph1,ph2]


def test(db_filename,test_data,table_name,table_creator):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    create_table(cursor,table_name,table_creator)
    att_str = att_string(table_creator)
    att_lst = att_list(att_str)
    insert_data(cursor,table_name,test_data,
                att_str,att_lst)
    connection.commit()


def test1():
    test('test.sqlite',dummy_data1(),'dummy',dummy_table_creator)


def test2():
    test('test.sqlite',dummy_data1(),'tracks',tracks_table_creator)


def test3():
    test('test.sqlite',dummy_data2(),'x_follows_y',x_follows_y_table_creator)
