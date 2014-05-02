import add_data as ad
import get_soundcloud_data as gsd
import sqlite3

class DbHandler(object):
    def __init__(self,db_name):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()

    def create_table(self,table_name):
        ad.create_table(self.curs,table_name)

    def write(self,table_name,data):
        ad.insert_tuple_data_set_into_DB(self.curs,table_name,data)
        self.conn.commit()

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

    def __init__(self,db_handler,limit=100):
        self.collected = set([])
        super(UserData,self).__init__(db_handler,limit)

    def extract(self,d,k):
        try:
            return d[k]
        except KeyError:
            return None

    def add_record(self,id,d):
        self.data.append([self.extract(d,v) for v in UserData.vars])
        self.collected.add(id)
        super(UserData,self).add_record(d)

    def update(self,d):
        for k,v in d.iteritems():
            self.add_record(k,d[k])


class FollowData(DataHandler):
    table = 'x_follows_y'
    vars=ad.att_list(ad.att_string(ad.tables[table]))

    def __init__(self,db_handler,limit=100):
        super(FollowData,self).__init__(db_handler,limit)

    def add_record(self,t):
        self.data.append(t)
        super(FollowData,self).add_record(t)

    def update(self,s):
        for t in s:
            self.add_record(t)


def user_dicts(resource):
    return {u.obj['id']:u.obj for u in resource.data}


def starting_user(user_id):
    return gsd.client.get('/users/' + str(user_id)).obj


def from_user(user_id):
    uid=str(user_id)
    follows = user_dicts(gsd.client.get('/users/'+ uid +'/followings'))
    followed_by = user_dicts(gsd.client.get('/users/'+ uid +'/followers'))
    x_follows_y=set([])
    for y in follows:
        x_follows_y.add((user_id,y))
    for x in followed_by:
        x_follows_y.add((x,user_id))
    follows.update(followed_by)
    return follows,x_follows_y


def from_users(user_list):
    user_data,x_follows_y = {},set([])
    for user in user_list:
        us,xfy = from_user(user)
        user_data.update(us)
        x_follows_y.update(xfy)
    return user_data, x_follows_y


def snowb(start_at,user_data,follow_data,folls_collected,steps):
    user_data.update({start_at:starting_user(start_at)})
    for i in range(steps):
        to_collect = user_data.collected - folls_collected
        ud,xfy = from_users(to_collect)
        user_data.update(ud)
        follow_data.update(xfy)
        folls_collected.update(to_collect)
    user_data.save()
    follow_data.save()
    return folls_collected


def collect(dbname,start_at,steps=1):
    dbh = DbHandler(dbname)
    dbh.create_table('users')
    dbh.create_table('x_follows_y')
    user_data = UserData(dbh,1)
    follow_data = FollowData(dbh,1)
    already_collected = set([])
    folls_collected = snowb(start_at,user_data,follow_data,
                            already_collected,steps)
    return folls_collected

def test(steps=1):
    collect('testit5.sqlite',202195,steps=steps)

