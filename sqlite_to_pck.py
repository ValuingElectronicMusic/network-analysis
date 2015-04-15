import cPickle
import sqlite3


def get_user_data(fn):
    conn=sqlite3.connect(fn)
    curs=conn.cursor()
    curs.execute('SELECT id,city,country,followers_count FROM users')
    return curs


def get_follows(fn):
    conn=sqlite3.connect(fn)
    curs=conn.cursor()
    curs.execute('SELECT follower,followed FROM x_follows_y')
    return curs


def convert_data(fn,seed_user):
    print 'Here we go...'
    follows=list(get_follows(fn))
    print 'Got follows.'
    sample=zip(*[f for f in follows if seed_user in f])
    sample=set(sample[0]+sample[1])
    print 'Established sample.'
    user_data=[u for u in get_user_data(fn) if u[0] in sample]
    print 'Got user data.'
    print 'Writing...'
    with open(fn+'.follows_{}.pck'.format(seed_user),'wb') as f:
        cPickle.dump(follows,f)
    print 'Follows written.'
    with open(fn+'.sample_{}.pck'.format(seed_user),'wb') as f:
        cPickle.dump(sample,f)
    print 'Sample written.'
    with open(fn+'.user_data_{}.pck'.format(seed_user),'wb') as f:
        cPickle.dump(user_data,f)
    print 'User data on sample members written.'
    print 'Written.'
