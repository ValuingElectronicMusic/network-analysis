# If you start collecting a wave and then regret it, you can use this
# to roll back the data collection. I would recommend duplicating the database
# first and letting this program loose on a copy, as you won't be able to
# get back any of the data you don't explicitly tell it to keep.

import sqlite3
import itertools
import add_data as ad


def rollback(db_path,waves_to_keep=[],waves_to_lose=[]):
    '''waves_to_keep and waves_to_lose should be lists of names of wave
    tables in the database currently being cleaned'''
    conn=sqlite3.connect(db_path)
    curs=conn.cursor()
    '''
    for wave in waves_to_lose:
        curs.execute('DROP TABLE {}'.format(wave))
    users_to_keep=[]
    for wave in waves_to_keep:
        curs.execute('SELECT id FROM {}'.format(wave))
        users_to_keep.extend(curs.fetchall())

    curs.execute('ALTER TABLE users RENAME TO old_users')
    ad.create_table(curs,'users')
    curs.execute('ALTER TABLE x_follows_y RENAME TO old_x_follows_y')
    ad.create_table(curs,'x_follows_y')

    follow_data=set([])
    
    for n, user in enumerate(users_to_keep):
        curs.execute('SELECT follower,followed FROM old_x_follows_y '
                     'WHERE follower=?',user)
        follow_data.update(curs.fetchall())
        curs.execute('SELECT follower,followed FROM old_x_follows_y '
                     'WHERE followed=?',user)
        follow_data.update(curs.fetchall())
        if n % 250 == 0: print "{} users' follow data read.".format(n)

    curs.executemany('INSERT INTO x_follows_y VALUES (?,?)', 
                     follow_data)
    conn.commit()
    print 'Cleaned x_follows_y table filled.'
    '''
    
    curs.execute('SELECT follower,followed FROM old_x_follows_y')
    follow_data=curs.fetchall()
    print 'Got follow data: {} follows'.format(len(follow_data))
    users_to_keep = set(itertools.chain.from_iterable(follow_data))
    print 'Got users from follow data: {} of them'.format(len(users_to_keep))

    print list(users_to_keep)[:10]

    n=0
    curs.execute('SELECT * FROM old_users')

    for i,user_data in enumerate(curs.fetchall()):

        if user_data[0] in users_to_keep:
            curs.execute('INSERT INTO users VALUES ('
                         '?,?,?,?,?,?,?,?,?,?,'
                         '?,?,?,?,?,?,?,?,?,?)',user_data)
            n+=1
        if i % 1000 == 0: 
            print '{}th user details checked.'.format(i)
        if n % 1000 == 0: 
            print '{}th user\'s details copied.'.format(n)

    print 'Gone through them all now'
    conn.commit()
    print 'Cleaned users table filled.'



