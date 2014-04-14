'''
Created on Apr 13, 2014

@author: daniel-allington
'''

# Adds to the _deriv database created in genre_relationships.py with a
# table from which corpora of comments can be pulled. Variables to
# determine whether a given comment will be added to a given corpus
# will be stored in this table too, for the sake of speed.

# Technically necessary to load the entire list of comment IDs into
# memory (can't just iterate through the comments table in the
# original database because this would be interrupted by other tasks
# for the cursor). Apart from that, trying to keep as little as
# possible in memory at a time through use of generators.

import deriv_db
import add_data


def corpus_table(cursderiv):
    add_data.create_table(cursderiv,'comments_corp')


def get_comment_ids(curssourc):
    curssourc.execute('SELECT id FROM comments')
    return curssourc.fetchall()

# Duplicate from genre_relationships. Delete, then merge.

def attribute_track(curssourc,track):
    curssourc.execute('SELECT user_id FROM tracks WHERE id=?',(track,))
    u=curssourc.fetchone()
    if u:
        return u[0]
    else:
        return u


def filtered(text):
    '''Placeholder for now. Will change @ usernames to a single @, numbers to
    a #, etc.'''
    return text


def language(text):
    '''Placeholder for now. Will attempt to identify language, using
    guess-language (install from pypi).'''
    return 'unknown'


def followsp(x,y,curssourc):
    return True


def favesp(x,t,curssourc):
    return True


def comment_data(curssourc,comment_id_list):
    for id in comment_id_list:
        sql='SELECT body,user_id,track_id,created_at FROM comments WHERE id=?'
        curssourc.execute(sql,(id[0],))
        c=curssourc.fetchone()
        creator=attribute_track(curssourc,c[2])
        x_fol_y=followsp(c[1],creator,curssourc)
        y_fol_x=followsp(creator,c[1],curssourc)
        x_fav_t=favesp(c[1],id[0],curssourc)
        filt=filtered(c[0])
        lang=language(filt)
        yield id[0],c[1],creator,x_fol_y,y_fol_x,x_fav_t,c[3],lang,filt


def add_comment_datum(cursderiv,comment):
    sql='INSERT INTO comments_corp VALUES (?,?,?,?,?,?,?,?,?)'
    cursderiv.execute(sql,comment)


def add_comment_data(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc=connsourc.cursor()
    cursderiv=connderiv.cursor()
    corpus_table(cursderiv)
    ids = get_comment_ids(curssourc)
    for comment in comment_data(curssourc,ids):
        add_comment_datum(cursderiv,comment)
    connderiv.commit()
