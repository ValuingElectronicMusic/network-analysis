'''
Created on Apr 1, 2014

@author: daniel-allington
'''

import sqlite3
import re


# Strings used for creating tables. As before, column names are names
# of attributes in SoundCloud data objects. For convenience, these are
# wrapped up in a dictionary.

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

# The following table creators are for the _deriv database.

gentag_table_creator='''string TEXT PRIMARY KEY, frequency INTEGER,
rank INTEGER'''

user_gentag_table_creator='''user INTEGER PRIMARY KEY, used TEXT,
most_used TEXT, most_used_three TEXT'''

x_faves_work_of_y_table_creator='''favourer INTEGER, favoured INTEGER, 
frequency INTEGER, PRIMARY KEY (favourer, favoured)'''

comments_corp_table_creator='''id INTEGER PRIMARY KEY, commenter INTEGER,
track_creator INTEGER, commenter_follows_creator INTEGER, 
creator_follows_commenter INTEGER, commenter_faves_track INTEGER, 
track_genre TEXT, track_tag_list TEXT, language TEXT, datetime TEXT, filtered_text TEXT'''

# Here's the dictionary containing all the table creators.

tables = {'tracks':tracks_table_creator, 'users':users_table_creator, 
'x_follows_y':x_follows_y_table_creator, 'groups':groups_table_creator,
'favourites':favourites_table_creator, 'comments':comments_table_creator,
'genres':gentag_table_creator, 'tags':gentag_table_creator,
'user_genres':user_gentag_table_creator, 'user_tags':user_gentag_table_creator,
'x_faves_work_of_y':x_faves_work_of_y_table_creator,
'comments_corp':comments_corp_table_creator}

# Here are sets containing table names; distinguish deriv database 
# from original.

table_names = {'tracks','users','x_follows_y','groups','favourites','comments'}
deriv_names = {'genres','tags','user_genres','user_tags','x_faves_work_of_y',
'comments_corp'}


# Generalised function for creating each of the tables we need, using
# strings such as the above. The table_name argument must be a key from
# the tables dictionary above

def create_table(cursor,table_name):
    cursor.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    cursor.execute('CREATE TABLE IF NOT '
                   'EXISTS {}({})'.format(table_name,tables[table_name]))


# Function to create all the tables we need for the original database
# (not the deriv database), using every table in the tables dictionary
# above.

def create_tables(db_filename):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    for table_name in table_names:
        create_table(cursor,table_name)
    connection.commit()


# Functions for turning table-creating string (above) into string
# of column names

def att_string(str):
    return re.sub(r'\n|[A-Z]|\(.*?\)','',str).strip(', ')


# Function for turning string of column names into list of column names
# (also assumed to be object attributes)

def att_list(att_str):
    return [att.strip() for att in att_str.split(',')]


# Function for getting data out of SoundCloud object, given list of
# the object's expected attributes. If an object lacks a particular
# attribute, returns NULL in place of that particular attribute's
# value

def obj_atts_list(obj, att_lst):
    l = []
    for att in att_lst:
        try:
            l.append(getattr(obj,att))
        except AttributeError:
            l.append('NULL')
    return l


# Generalised function for putting data into tables created above. As
# with create_table, the table_name argument must be a key from the
# tables dictionary above. Uses exception handling to stop attempts
# to insert a row with a primary key that already exists.

def insert_data(cursor,table_name,data):
    att_str=att_string(tables[table_name])
    att_lst=att_list(att_str)
    sql=('INSERT INTO {} ({}) '
         'VALUES({})'.format(table_name,att_str,('?, '*len(att_lst))[:-2]))
    vals_list = [tuple(obj_atts_list(d,att_lst)) for d in data]
    for vals in vals_list:
        try:
            cursor.execute(sql,vals)
        except sqlite3.IntegrityError:
            pass

def insert_deriv_data(cursor,table_name,data):
    att_str=att_string(tables[table_name])
    att_lst=att_list(att_str)
    sql=('INSERT INTO {} ({}) '
         'VALUES({})'.format(table_name,att_str,('?, '*len(att_lst))[:-2]))
    for d in data:
        cursor.execute(sql,d)


# Unit tests follow. test1() and test2() will create a database with
# two tables, one of which will contain null values where the objects
# from which the data was drawn lacked expected attributes.

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


def test(db_filename,test_data,table_name):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    create_table(cursor,table_name)
    insert_data(cursor,table_name,test_data)
    connection.commit()


def test1():
    test('test.sqlite',dummy_data1(),'tracks')


def test2():
    test('test.sqlite',dummy_data2(),'x_follows_y')
