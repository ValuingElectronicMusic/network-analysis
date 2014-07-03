# Like get_minimal.py, but without the memory overhead: uses text files
# as buffers instead, and works through everything no more than a few
# items at a time. Now also has logging and time delay, mostly cribbed
# from get_soundcloud_data.py, although with a few changes.

import add_data as ad
import get_soundcloud_data as gsd
import genre_relationships as gr
import sqlite3
import time
import logging

db_path = 'minim/data/'
log_path = 'minim/logs/'
tmp_path = 'minim/temp/'
time_delay = 2
max_attempts = 100


def time_stamp():
    return time.strftime('%Y%m%d-%H%M')


class DbHandler(object):
    def __init__(self,db_name,logger):
        self.ts = time_stamp()
        self.db_path = db_path+db_name+'.sqlite'
        self.conn = sqlite3.connect(self.db_path)
        self.curs = self.conn.cursor()
        self.logger=logger

    def create_table(self,table_name):
        ad.create_table(self.curs,table_name)

    def create_tables_if_needed(self,table_list):
        present = gr.check_tables(self.curs,table_list)
        for n,t in enumerate(present):
            tn = table_list[n]
            if t: 
                self.logger.info('{} table is present'.format(tn))
            else:
                self.logger.info('Creating table: {}'.format(tn))
                self.create_table(tn)

    def write(self,table_name,data):
        self.logger.info('sending {} items to {}.'.format(len(data),
                                                          table_name))
        ad.insert_tuple_data_set_into_DB(self.curs,table_name,data)
        self.conn.commit()

    def collected_users(self):
        fn=tmp_path+'collected_users'+self.ts+'.txt'
        self.logger.info('writing list of collected users to '
                         '{}'.format(fn))
        all_users = open(fn,'w')
        for r in self.curs.execute('SELECT id FROM users'):
            all_users.write(str(r[0])+'\n')
        all_users.close()
        return open(fn,'r')

    def collected_followers(self,user):
        self.curs.execute('SELECT * FROM x_follows_y '
                          'WHERE followed=?',(user,))
        return len(self.curs.fetchall())

    def collected_followings(self,user):
        self.curs.execute('SELECT * FROM x_follows_y '
                          'WHERE follower=?',(user,))
        return len(self.curs.fetchall())

    def total_followers(self,user):
        return self.curs.execute('SELECT "followers_count" '
                                 'FROM users WHERE id=?',(user,)).next()[0]

    def total_followings(self,user):
        return self.curs.execute('SELECT "followings_count" '
                                 'FROM users WHERE id=?',(user,)).next()[0]

class DataHandler(object):
    table = ''
    vars = []

    def __init__(self,db_handler,limit):
        self.db_handler = db_handler
        self.limit = limit
        self.data = []

    def clear(self):
        self.data = []

    def save(self):
        self.db_handler.write(self.table,self.data)
        self.clear()

    def add_record(self,r):
        if len(self.data) >= self.limit: self.save()


class UserData(DataHandler):
    table = 'users'
    vars=ad.att_list(ad.att_string(ad.tables[table]))

    def __init__(self,dbh,limit=1):
        self._collected = open(tmp_path+'now_collected'+dbh.ts+'.txt','w+')
        super(UserData,self).__init__(dbh,limit)

    @property
    def collected(self):
        self._collected.seek(0)
        return self._collected

    def add_to_collected(self,datum):
        self._collected.seek(0,2)
        self._collected.write(str(datum)+'\n')

    def extract(self,d,k):
        try:
            return d[k]
        except KeyError:
            return None

    def add_record(self,id,d):
        self.data.append([self.extract(d,v) for v in UserData.vars])
        self.add_to_collected(id)
        super(UserData,self).add_record(d)

    def update(self,d):
        for k,v in d.iteritems():
            self.add_record(k,d[k])


class FollowData(DataHandler):
    table = 'x_follows_y'
    vars=ad.att_list(ad.att_string(ad.tables[table]))

    def __init__(self,db_handler,limit=1):
        super(FollowData,self).__init__(db_handler,limit)

    def add_record(self,t):
        self.data.append(t)
        super(FollowData,self).add_record(t)

    def update(self,s):
        for t in s:
            self.add_record(t)


def user_dicts(resource):
    return {u.obj['id']:u.obj for u in resource.data}


def get_data(req,dbh):
    count1 = 1
    while True:
        count2 = 1
        while count2 < max_attempts:
            try:
                return user_dicts(gsd.client.get(req),
                                  limit=200)
            # Could turn the above into a loop that keeps calling the API
            # with a successively higher offset keyword argument until
            # fewer than 200 results are returned. BUT this would mean
            # that the program ended up spending an inordinate amount of
            # time downloading Justin Timberlake's 5 million followers.
            # Perhaps we should stop collecting followers and collect
            # followings only - as nobody follows 5 million people. This
            # would also be an easy way of avoiding useless collection
            # of bot accounts.

            # THAT SAID, I've checked and there seems to be a limit of
            # 2000 on followings: about 1 in 60 of the accounts I've
            # collected follows exactly 2000 other accounts. Which is
            # somewhat artificial (a very small number follow just over
            # 2000 - I wonder if the limit was imposed at a certain point
            # in time).

            except Exception as e:
                warning = ('ERROR in client.get() - problem connecting to '
                           'SoundCloud API, error '+str(e)+' for '
                           'request '+req+'. Trying again... '
                           'attempt '+str(count2)+' of '+str(max_attempts))
                print warning
                dbh.logger.warning(warning)
                time.sleep(time_delay)
                count2 += 1
        big_delay = count1 * 600
        warning = ('Max attempts exceeded. Waiting '
                   '{} minutes before resuming.'.format(big_delay*10))
        print warning
        dbh.logger.warning(warning)
        time.sleep(big_delay)
        count1 += 1


def starting_user(user_id,dbh):
    return get_data('/users/' + str(user_id),dbh).obj


def follows_user(user_id,dbh):
    follows = user_dicts(get_data('/users/'+str(user_id)+'/followers',dbh))
    x_follows_y = {(x,user_id) for x in follows}
    return follows,x_follows_y


def followed_by_user(user_id,dbh):
    followed_by = user_dicts(get_data('/users/'+ str(user_id) +'/followings',dbh))
    x_follows_y = {(user_id,y) for y in followed_by}
    return followed_by,x_follows_y


def collect_from_users(to_collect_followers,to_collect_following,
                       collected_followers,collected_following,
                       user_data,x_follows_y,dbh):
    for user in to_collect_followers:
        us,xfy = follows_user(user,dbh)
        user_data.update(us)
        x_follows_y.update(xfy)
        collected_followers.write(str(user))
    collected_followers.seek(0)
    for user in to_collect_following:
        us,xfy = followed_by_user(user,dbh)
        user_data.update(us)
        x_follows_y.update(xfy)
        collected_following.write(str(user))
    collected_following.seek(0)

def collected(dbh,thresh):
    cu = dbh.collected_users()
    fn_followers=tmp_path+'collected_followers'+dbh.ts+'.txt'
    fn_following=tmp_path+'collected_following'+dbh.ts+'.txt'
    collected_followers=open(fn_followers,'w')
    collected_following=open(fn_following,'w')
    for u in cu:
        l = '{}\n'.format(u)
        if dbh.collected_followers(u) >= dbh.total_followers(u) * thresh:
            collected_followers.write(l)
        if dbh.collected_followings(u) >= (dbh.total_followings(u) * thresh):
            collected_following.write(l)
    collected_followers.close()
    collected_following.close()
    collected_followers=open(fn_followers,'r+')
    collected_following=open(fn_following,'r+')
    return collected_followers,collected_following


def to_collect(user_data,collected_followers,collected_following,dbh):
    fn_followers=tmp_path+'to_collect_followers'+dbh.ts+'.txt'
    fn_following=tmp_path+'to_collect_following'+dbh.ts+'.txt'
    to_collect_followers = open(fn_followers,'w')
    to_collect_following = open(fn_following,'w')
    for user in user_data.collected:
        if user not in collected_followers:
            to_collect_followers.write(user)
        if user not in collected_following:
            to_collect_following.write(user)
    to_collect_followers.close()
    to_collect_following.close()
    collected_followers = open(fn_followers,'r')
    collected_following = open(fn_following,'r')
    return collected_followers,collected_following


def snowb(start_at,dbh,user_data,follow_data,steps,thresh):
    dbh.logger.info('Starting user: {}'.format(start_at))
    user_data.update({start_at:starting_user(start_at,dbh)})
    collected_followers,collected_following = collected(dbh,thresh)
    for step in range(steps):
        dbh.logger.info('Degrees of separation from '
                        '{}: {}'.format(start_at,step+1))
        if step==0:
            to_collect_followers,to_collect_following = [start_at],[start_at]
        else:
            (to_collect_followers,
             to_collect_following) = to_collect(user_data,
                                                collected_followers,
                                                collected_following,
                                                dbh)
        collect_from_users(to_collect_followers,to_collect_following,
                           collected_followers,collected_following,
                           user_data,follow_data,dbh)
        user_data.save()
        follow_data.save()
    return (to_collect_followers,to_collect_following,
            collected_followers,collected_following,
            user_data,follow_data)


def collect(dbname,start_at,steps=1,thresh=0.5):
    ts = time_stamp()
    loghandler=logging.FileHandler(log_path+ts+'.log')
    logformatter=logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    loghandler.setFormatter(logformatter)
    logger=logging.getLogger('minim')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(loghandler)
    logger.info('Here we go...')
    dbh = DbHandler(dbname,logger)
    dbh.create_tables_if_needed(['users','x_follows_y'])
    user_data = UserData(dbh,50)
    follow_data = FollowData(dbh,50)
    return snowb(start_at,dbh,user_data,follow_data,
                        steps,thresh)


Slackk = 202195
Sephirot = 81070
Sculpture = 261433 # actual username is tapebox 
Ms_Skyrym = 15899888


def test(steps=1):
    collect('testit4',Sculpture,steps=steps)

