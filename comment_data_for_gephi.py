# Create CSV file for import into Gephi

import sqlite3
import csv
import codecs
import collections


def cursor(db_fn):
    conn=sqlite3.connect(db_fn+'.sqlite')
    return conn.cursor()


def write_csv(fn,csv_data):
    f=codecs.open(fn,'wb','utf-8')
    csv_writer = csv.writer(f, delimiter=';',
                            quoting=csv.QUOTE_NONE)
    csv_writer.writerows(csv_data)


def arc_csv(curs,nodes=False):
    yield 'Source','Target','DateTime'
    curs.execute('SELECT user_id,track_id,created_at FROM comments')
    comments=curs.fetchall()
    if nodes: comments=[comment for comment in comments if comment[0] in nodes]
    for comment in comments:
        curs.execute('SELECT user_id FROM tracks WHERE id=?',(comment[1],))
        commented_on=curs.fetchone()[0]
        if comment[0]!=int(commented_on):
            yield comment[0],commented_on,comment[2]


def csv_file(db_fn,csv_fn,exclude_outsiders):
    curs=cursor(db_fn)
    arc_fn=csv_fn+'_arcs.csv'
    curs.execute('SELECT id FROM users')
    if exclude_outsiders: nodes=[n[0] for n in curs.fetchall()]
    else: nodes=False
    write_csv(arc_fn,arc_csv(curs,nodes))


def test(exclude_outsiders=False):
    writepath='comment_interactions/'
    readpath='comment_interactions/'
    db_fn='seed_81070_20140602_1852'
    csv_fn='sephiroth_plus_20'
    csv_file(readpath+db_fn,writepath+csv_fn,exclude_outsiders)

