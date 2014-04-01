import sqlite3
import string

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


def att_string(str):
    return str.translate(None,string.ascii_uppercase)


def att_list(att_str):
    return [att.strip() for att in att_str.split(',')]


def obj_atts_list(obj, att_list):
    l = []
    for att in att_list:
        try:
            l.append(getattr(obj,att))
        except AttributeError:
            l.append('NULL')
    return l


def add_data(cursor, table, data, att_list):
    sql='INSERT INTO {} VALUES({})'.format(table,('?, '*len(att_list))[:-2])

    for datum in data:
        try:
            vals=tuple(obj_atts_list(datum,att_list))
            cursor.execute(sql,vals)
        except Exception as e:
            print('Error adding {} to '
                  '{}: {} {}'.format(datum.id,table,e.message,e.args))


# Unit tests follow

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
    conn = sqlite3.connect('test1.sqlite')
    curs = conn.cursor()
    curs.execute('DROP TABLE IF EXISTS dummy')
    curs.execute('CREATE TABLE IF NOT '
                 'EXISTS dummy({})'.format(dummy_table_creator))
    add_data(curs,'dummy',test_data,att_list(att_string(dummy_table_creator)))
    conn.commit()


def test2():
    test_data = dummy_data()
    conn = sqlite3.connect('test2.sqlite')
    curs = conn.cursor()
    curs.execute('DROP TABLE IF EXISTS tracks')
    curs.execute('CREATE TABLE IF NOT '
                 'EXISTS tracks({})'.format(tracks_table_creator))
    add_data(curs,'tracks',test_data,
             att_list(att_string(tracks_table_creator)))
    conn.commit()
