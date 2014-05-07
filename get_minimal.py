import add_data as ad
import get_soundcloud_data as gsd
import genre_relationships as gr
import sqlite3

class DbHandler(object):
    def __init__(self,db_name):
        self.conn = sqlite3.connect(db_name)
        self.curs = self.conn.cursor()

    def create_table(self,table_name):
        ad.create_table(self.curs,table_name)

    def create_tables_if_needed(self,table_list):
        present = gr.check_tables(self.curs,table_list)
        for n,t in enumerate(present):
            if not t: self.create_table(table_list[n])

    def write(self,table_name,data):
        ad.insert_tuple_data_set_into_DB(self.curs,table_name,data)
        self.conn.commit()

    def collected_users(self):
        self.curs.execute('SELECT id FROM users')
        return [r[0] for r in self.curs.fetchall()]

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


def follows_user(user_id):
    follows = user_dicts(gsd.client.get('/users/'+ str(user_id) +'/followers'))
    x_follows_y = {(x,user_id) for x in follows}
    return follows,x_follows_y


def followed_by_user(user_id):
    followed_by = user_dicts(gsd.client.get('/users/'+ str(user_id) +'/followings'))
    x_follows_y = {(user_id,y) for y in followed_by}
    return followed_by,x_follows_y


def from_users(collect_followers,collect_following):
    user_data,x_follows_y = {},set([])
    for user in collect_followers:
        us,xfy = follows_user(user)
        user_data.update(us)
        x_follows_y.update(xfy)
    for user in collect_following:
        us,xfy = followed_by_user(user)
        user_data.update(us)
        x_follows_y.update(xfy)
    return user_data, x_follows_y


def collected(dbh,thresh):
    cu = dbh.collected_users()
    collected_followers = {u for u in cu if dbh.collected_followers(u) 
                           >= (dbh.total_followers(u) * thresh)}
    collected_following = {u for u in cu if dbh.collected_followings(u) 
                           >= (dbh.total_followings(u) * thresh)}
    return collected_followers,collected_following


def to_collect(user_data,collected_followers,collected_following):
    return (user_data.collected - collected_followers,
            user_data.collected - collected_following)


def snowb(start_at,dbh,user_data,follow_data,steps,thresh):
    user_data.update({start_at:starting_user(start_at)})
    collected_followers,collected_following = collected(dbh,thresh)
    for i in range(steps):
        if i==0:
            to_collect_followers,to_collect_following = {start_at},{start_at}
        else:
            (to_collect_followers,
             to_collect_following) = to_collect(user_data,
                                                collected_followers,
                                                collected_following)
        ud,xfy = from_users(to_collect_followers,to_collect_following)
        user_data.update(ud)
        follow_data.update(xfy)
        collected_followers.update(to_collect_followers)
        collected_following.update(to_collect_following)
    return user_data,follow_data


def collect(dbname,start_at,steps=1,thresh=0.5):
    dbh = DbHandler(dbname)
    dbh.create_tables_if_needed(['users','x_follows_y'])
    user_data = UserData(dbh,50)
    follow_data = FollowData(dbh,50)
    return snowb(start_at,dbh,user_data,follow_data,
                        steps,thresh)


Slackk = 202195
Sephirot = 81070
Ms_Skyrym = 15899888


def test(steps=1):
    return collect('testit7.sqlite',Ms_Skyrym,steps=steps)

