'''
Created on Apr 13, 2014

@author: daniel-allington
'''

# Adds to the _deriv databse created in genre_relationships.py with a
# table from which corpora of comments can be pulled.

import deriv_db
import add_data


def faves_table(cursderiv):
    add_data.create_table(cursderiv,'x_faves_work_of_y')


def get_faves(curssourc):
    curssourc.execute('SELECT user_id,track_id FROM favourites')
    return curssourc.fetchall()


def attribute_track(curssourc,track):
    curssourc.execute('SELECT user_id FROM tracks WHERE id=?',(track,))
    u=curssourc.fetchone()
    if u:
        return u[0]
    else:
        return u


def fave_relations(curssourc,fave_list):
    for fave in fave_list:
        yield fave[0],attribute_track(curssourc,fave[1])


def update_fave_table(cursderiv,fave):
    sql=('SELECT frequency FROM x_faves_work_of_y WHERE favourer=? '
         'AND favoured=?')
    cursderiv.execute(sql,(fave[0],fave[1]))
    f=cursderiv.fetchone()
    if f:
        sql='UPDATE x_faves_work_of_y SET frequency=? WHERE favourer=? AND favoured=?'
        cursderiv.execute(sql,(f[0]+1,fave[0],fave[1]))
    else:
        sql='INSERT INTO x_faves_work_of_y VALUES (?,?,1)'
        cursderiv.execute(sql,(fave[0],fave[1]))


def add_fave_relations(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc=connsourc.cursor()
    cursderiv=connderiv.cursor()
    faves_table(cursderiv)
    unaccounted=0
    done=0
    for fave in fave_relations(curssourc,get_faves(curssourc)):
        if fave[1]:
            update_fave_table(cursderiv,fave)
            done+=1
            if done%1000==0: 
                connderiv.commit()
                print 'Done: '+str(done)
    connderiv.commit()
    print 'Done: '+str(done)
