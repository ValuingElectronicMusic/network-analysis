# Like forward_waves.py, but collects followers and followees of each
# individual. The number of 'waves' is the maximum number of degrees
# of separation from the seed, plus one (since the seed is collected
# in the first wave). Note that limitations of the SoundCloud API will
# prevent all followers of an individual being collected where there
# are over 8199 such followers.

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
buffer_size = 500


def time_stamp():
    return time.strftime('%Y%m%d_%H%M')


class DbHandler(object):
    def __init__(self,db_name,seed,totalwaves,startwave,logger):
        self.ts = time_stamp()
        self.db_path = db_path+db_name+'.sqlite'
        self.seed = seed
        self.conn = sqlite3.connect(self.db_path)
        self.curs = self.conn.cursor()
        self.logger=logger
        self.beginning_wave=startwave
        self.current_wave=startwave
        self.highest_wave_table=totalwaves
        self.wave_tables=self.create_wave_tables()

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

    def create_wave_tables(self):
        wave_tables = {}
        if self.beginning_wave !=0:
            for wave in range(self.highest_wave_table+1):
                table = 'from_{}_degree_{}'.format(self.seed,wave)
                wave_tables[wave]=table
        start = (0 if self.beginning_wave==0 else self.beginning_wave+1)
        stop = self.highest_wave_table+1
        for wave in range(start,stop):
            table = 'from_{}_degree_{}'.format(self.seed,wave)
            self.logger.info('Creating wave table: {}'.format(table))
            self.curs.execute('DROP TABLE IF EXISTS "{}"'.format(table))
            self.curs.execute('CREATE TABLE "{}" '
                              '(id INTEGER PRIMARY KEY)'.format(table))
            wave_tables[wave]=table
        if self.beginning_wave==0:
            self.curs.execute('INSERT INTO {} '
                              'VALUES({})'.format(wave_tables[0],self.seed))
        return wave_tables

    def this_wave(self):
        sql = 'SELECT id FROM {}'.format(self.wave_tables[self.current_wave])
        return (u[0] for u in self.curs.execute(sql))

    def collectedp(self,id):
        for i in range(self.current_wave+1):
            sql=('SELECT count(1) FROM {} '
                 'WHERE id=?'.format(self.wave_tables[i]))
            if self.curs.execute(sql,(id,)).next()[0]:
                return True

    def create_next_wave(self,this_wave):
        next_table = self.wave_tables[self.current_wave+1]
        self.logger.info('Filling wave table: '
                         '{}'.format(next_table))
        sql1 = 'SELECT followed FROM x_follows_y WHERE follower=?'
        sql2 = 'SELECT follower FROM x_follows_y where followed=?'
        for user in this_wave:
            for query in [sql1,sql2]:
                self.curs.execute(query,(user,))
                for connected in self.curs.fetchall():
                    if not self.collectedp(connected[0]):
                        sql3 = ('INSERT INTO "{}" '
                                'VALUES ({})'.format(next_table,connected[0]))
                        try:
                            self.curs.execute(sql3)
                        except sqlite3.IntegrityError:
                            pass
        self.conn.commit()

    def write(self,table_name,data):
        self.logger.info('Sending {} items to {}.'.format(len(data),
                                                          table_name))
        ad.insert_tuple_data_set_into_DB(self.curs,table_name,data)
        self.conn.commit()

    def to_collect(self):
        fn=tmp_path+self.ts+'_wave_'+str(self.current_wave)+'.tmp'
        to_collect = open(fn,'w')
        for user in self.this_wave():
            to_collect.write(str(user)+'\n')
        to_collect.close()
        return open(fn,'r')


class DataHandler(object):
    table = ''
    vars = []

    def __init__(self,db_handler):
        self.db_handler = db_handler
        self.limit = buffer_size
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

    def __init__(self,dbh):
        super(UserData,self).__init__(dbh)

    def extract(self,d,k):
        try:
            return d[k]
        except KeyError:
            return None

    def add_record(self,id,d):
        self.data.append([self.extract(d,v) for v in UserData.vars])
        super(UserData,self).add_record(d)

    def update(self,d):
        for k,v in d.iteritems():
            self.add_record(k,d[k])

                              
class FollowData(DataHandler):
    table = 'x_follows_y'
    vars=ad.att_list(ad.att_string(ad.tables[table]))

    def __init__(self,db_handler):
        super(FollowData,self).__init__(db_handler)
        
    def add_record(self,t):
        self.data.append(t)
        super(FollowData,self).add_record(t)

    def update(self,s):
        for t in s:
            self.add_record(t)


def user_dicts(resourcelist):
    return {u.obj['id']:u.obj for u in resourcelist}


def get_data(req,dbh):
    '''Mostly copied from all_data_one_person.py'''
    collected = {}
    start_at = 0
    batch_length = 199
    while batch_length > 198 and start_at < 8001:
        count = 1
        mouthful = 199
        while True:
            try:
                if req[-1].isdigit():
                    return gsd.client.get(req)
                else:
                    batch=user_dicts(gsd.client.get(req,
                                                    order='created_at', 
                                                    limit=mouthful,
                                                    offset=start_at))
                    collected.update(batch)
                    batch_length = len(batch)
                    start_at += mouthful
                    break
            except Exception as e:
                warning = ('ERROR in client.get() - problem connecting to '
                           'SoundCloud API, error '+str(e)+' for '
                           'request '+req+', limit='+str(mouthful)+
                           ', offset='+str(start_at)+'. Trying again... '
                           'attempt '+str(count))
                dbh.logger.warning(warning)
                print warning

                if str(e)[:3]=='404': # non-existent user ID
                    return None

                if str(e)[:3]=='500': # too much data for server
                    mouthful = mouthful / 2
                    if mouthful < 1: mouthful = 1

                time.sleep(time_delay * count)
                count += 1
    return collected


def starting_user(user_id,dbh):
    return get_data('/users/'+str(user_id),dbh).obj


def connected_to_user(user_id,dbh,collect_followers):
    req='/users/{}/followings'.format(user_id)
    follow_accounts = get_data(req,dbh)
    x_follows_y = {(user_id,y) for y in follow_accounts}
    if collect_followers:
        req='/users/{}/followers'.format(user_id)
        followers = get_data(req,dbh)
        x_follows_y = x_follows_y | {(x,user_id) for x in followers}
        follow_accounts.update(followers)
    return dict(follow_accounts),x_follows_y


def collect_from_users(connected_to_collect,
                       user_data,x_follows_y,dbh,collect_followers):
    for user in connected_to_collect:
        us,xfy = connected_to_user(int(user),dbh,collect_followers)
        user_data.update(us)
        x_follows_y.update(xfy)


def now_where_was_i(fn,pickup_user):
    f=open(fn,'r')
    s='\n{}\n'.format(pickup_user)
    l=len(s)
    found=False
    buffer='\n'+f.read(l-1)
    while not found:
        if buffer==s:
            found=f.tell()
        c=f.read(1)
        if not c: break
        buffer=buffer[1:]+c
    if found:
        f.seek(found-l+1,0)
        return f
    print 'User not found in tempfile.'


def roll_snowball(seed,dbh,user_data,follow_data,totalwaves,startwave,
                  tempfile=False,pickup_user=False):
    dbh.logger.info('Starting user: {}'.format(seed))
    user_data.update({seed:starting_user(seed,dbh)})
    for wave in range(startwave,totalwaves):
        dbh.current_wave=wave
        message = 'Wave: {}'.format(wave)
        dbh.logger.info(message)
        print message
        if wave==startwave and tempfile and pickup_user:
            this_wave=now_where_was_i(tempfile,pickup_user)
        elif wave==startwave and tempfile and not pickup_user:
            this_wave=open(tempfile,'r')
        else:
            this_wave=dbh.to_collect()
        if wave==startwave or wave < totalwaves-1:
            collect_followers=True
        else:
            collect_followers=False
        collect_from_users(this_wave,user_data,follow_data,dbh,
                           collect_followers)
        user_data.save()

        follow_data.save()
        this_wave.seek(0)
        message = 'Wave {} complete'.format(wave)
        dbh.logger.info(message)
        print message
        dbh.create_next_wave(this_wave)
    return (user_data,follow_data)


def log_writer(ts):
    loghandler=logging.FileHandler(log_path+ts+'.log')
    logformatter=logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
    loghandler.setFormatter(logformatter)
    logger=logging.getLogger('minim')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(loghandler)
    logger.info('Here we go...')
    return logger


def collect(dbname,seed,waves=1):
    ts = time_stamp()
    logger = log_writer(ts)
    dbh = DbHandler(dbname,seed,waves,0,logger)
    dbh.create_tables_if_needed(['users','x_follows_y'])
    user_data = UserData(dbh)
    follow_data = FollowData(dbh)
    return roll_snowball(seed,dbh,user_data,follow_data,
                         waves,0)

def resume(dbname,seed,totalwaves,startwave,tempfile=False,pickup_user=False):
    ts=time_stamp()
    logger = log_writer(ts)
    dbh = DbHandler(dbname,seed,totalwaves,startwave,logger)
    user_data = UserData(dbh)
    follow_data = FollowData(dbh)
    return roll_snowball(seed,dbh,user_data,follow_data,
                         totalwaves,startwave,tempfile,pickup_user)


Slackk = ('slackk',202195)
Sephirot = ('sephirot',81070)
Sculpture = ('tapebox',261433)
Ms_Skyrym = ('theresa-deane-1',15899888)
FAS = ('fas',55078931)
Rob_Tubb = ('cminer',271933)
Mr_Mitch = ('mrmitchmusic',88257)
Josh_Shirt = ('shirty',18489)
Cursor_Miner = ('cminer',271933)


case_studies = [Josh_Shirt,Cursor_Miner]


def ego_nets(seeds=case_studies,waves=2):
    for seed in seeds:
        print 'Current seed: {}.'.format(seed[0])
        collect('ego_net_of_{}'.format(seed[0]),seed[1],waves=waves)

