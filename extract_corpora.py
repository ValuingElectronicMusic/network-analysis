# Create CSV file for correspondence analysis: co-occurrence of genre
# or tag strings

import sqlite3
import codecs

def cursor(fn):
    conn=sqlite3.connect(fn)
    return conn.cursor()


def hipcorp(curs):
    return curs.execute('SELECT filtered_text FROM comments_corp '
                        'WHERE language=1 '
                        'AND track_genre LIKE "%hip%hop%"')

def housecorp(curs):
    return curs.execute('SELECT filtered_text FROM comments_corp '
                        'WHERE language=1 '
                        'AND track_genre LIKE "%house%"')

def extract():
    curs=cursor('vis/scdb20140501-1106current_deriv.sqlite')
    for filen,func in [('hipcorp.txt',hipcorp),
                       ('housecorp.txt',housecorp)]:
        with codecs.open(filen,'w','utf-8-sig') as f:
            for t in func(curs):
                f.write(t[0]+u'\n\n')
