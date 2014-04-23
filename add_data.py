'''
Created on Apr 1, 2014

@author: daniel-allington
'''

import sqlite3
import re


# Strings used for creating tables. As before, column names are names
# of attributes in SoundCloud data objects. For convenience, these are
# wrapped up in a dictionary.
#
# For definitions of column names, see:
#     http://developers.soundcloud.com/docs/api/reference

users_table_creator='''id INTEGER PRIMARY KEY, username TEXT, 
first_name TEXT, last_name TEXT, full_name TEXT, 
permalink_url TEXT, description TEXT, plan TEXT, 
city TEXT, country TEXT, 
track_count INTEGER, playlist_count INTEGER, public_favorites_count INTEGER, 
followers_count INTEGER, followings_count INTEGER,
website TEXT, website_title TEXT, 
avatar_url TEXT, discogs_name TEXT, myspace_name TEXT, subscriptions TEXT'''

tracks_table_creator='''id INTEGER PRIMARY KEY, user_id TEXT,  
title TEXT, permalink_url TEXT, description TEXT, tag_list TEXT, state TEXT,
duration INTEGER, genre TEXT,  key_signature TEXT, bpm INTEGER,  
original_content_size INTEGER, original_format TEXT, track_type TEXT,    
sharing TEXT, streamable TEXT, embeddable_by TEXT, downloadable TEXT, commentable TEXT,
release INTEGER, release_year INTEGER, release_month INTEGER, release_day INTEGER,
purchase_title TEXT, purchase_url TEXT, label_id TEXT, label_name TEXT, license TEXT, 
isrc TEXT, video_url TEXT, artwork_url TEXT, 
waveform_url TEXT, stream_url TEXT, attachments_uri TEXT,
playback_count INTEGER, download_count INTEGER, 
favoritings_count INTEGER, comment_count INTEGER, 
created_at TEXT, created_using_permalink_url TEXT'''

x_follows_y_table_creator='''follower INTEGER, followed INTEGER, 
PRIMARY KEY (follower, followed)'''

favourites_table_creator='''user_id INTEGER, track_id INTEGER, track_producer_id INTEGER, 
PRIMARY KEY (user_id, track_id)'''

group_mem_table_creator='''user_id INTEGER, group_id INTEGER, 
PRIMARY KEY (user_id, group_id)'''

groups_table_creator='''id INTEGER PRIMARY KEY, name TEXT, 
created_at TEXT, creator_id INTEGER, moderated TEXT, 
short_description TEXT, description TEXT, permalink_url TEXT,  
track_count INTEGER, members_count INTEGER, contributors_count INTEGER,  
artwork_url TEXT'''

comments_table_creator='''id INTEGER PRIMARY KEY, user_id INTEGER, track_id INTEGER, 
body TEXT, timestamp INTEGER, created_at TEXT, uri TEXT'''
      
playlists_table_creator='''user_id INTEGER, playlist_id INTEGER, track_id INTEGER, 
track_producer_id INTEGER, PRIMARY KEY(playlist_id, track_id)'''


# The following table creators are for the _deriv database.
# TODO AJ: I think this should go somewhere separate? Not currently used?

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
'x_follows_y':x_follows_y_table_creator, 'favourites':favourites_table_creator, 
'group_mem':group_mem_table_creator, 'groups':groups_table_creator,   
'comments':comments_table_creator, 'playlists':playlists_table_creator,
'genres':gentag_table_creator, 'tags':gentag_table_creator,
'user_genres':user_gentag_table_creator, 'user_tags':user_gentag_table_creator,
'x_faves_work_of_y':x_faves_work_of_y_table_creator,
'comments_corp':comments_corp_table_creator}

# Here are sets containing table names; distinguish deriv database 
# from original.
# Minor edit - declaring sets as set([...]0 rather than using curly brackets
# for backwards compatability
table_names = set(['tracks','users','x_follows_y','groups','group_mem','favourites','comments','playlists'])
deriv_names = set(['genres','tags','user_genres','user_tags','x_faves_work_of_y','comments_corp'])


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

def att_string(strng):
    return re.sub(r'\n|[A-Z]|\(.*?\)','',strng).strip(', ')


# Function for turning string of column names into list of column names
# (also assumed to be object attributes)

def att_list(att_str):
    return [att.strip() for att in att_str.split(',')]


# Function for getting data out of SoundCloud object, given list of
# the object's expected attributes. If an object lacks a particular
# attribute, returns None in place of that particular attribute's
# value (which is then automatically translated into NULL when passed
# to the SQLite database).

def obj_atts_list(obj, att_lst):
    l = []
    for att in att_lst:
        # AJ added
        # Some attributes are not plain attributes but are themselves
        # specific sub-attributes of a attribute_dict
        # As shorthand, these are indicated in the _table_creator fields
        # using a double underscore __ . 
        # Find and deal with retrieving these data separately  
#         if ('__' in att):
#             att_rep = att.replace('__', ',')
#              split att around the '__' divider
#             att_rep_spl = [a.strip() for a in att_rep.split(',')]
#             try:
#                 container_dict = getattr(obj,att_rep_spl[0])
#                 l.append(container_dict.get(att_rep_spl[1],None))
#                  
#             except AttributeError:
#                 l.append(None)
#         else:
        try:
            l.append(getattr(obj,att))
        except AttributeError:
            l.append(None)
    return l


# Generalised function for putting data into tables created above. As
# with create_table, the table_name argument must be a key from the
# tables dictionary above. Uses exception handling to stop attempts
# to insert a row with a primary key that already exists (should be
# much faster than checking before inserting). Will fail if there are
# any other errors - but that's the Pythonic way to do it as we will
# want a stack trace etc.

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


# This one is for inserting into the _deriv database.

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
    return set([ph1,ph2])  # AJ slight edit - needs to work with sets


def dummy_data2():
    ph1 = placeholder()
    ph1.follower = 12345
    ph1.followed = 67890
    ph2 = placeholder()
    ph2.follower = 67890
    ph2.followed = 12345
    return set([ph1,ph2])


def test(db_filename,test_data,table_name):
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    create_table(cursor,table_name)
    insert_data(cursor,table_name,test_data)
    connection.commit()


def test1():
    test('test1.sqlite',dummy_data1(),'tracks')


def test2():
    test('test2.sqlite',dummy_data2(),'x_follows_y')
    
if __name__ == '__main__':
    test1()
    test2()
