#!/usr/bin/env python

# This comprises a function to get all the data out of the sqlite
# table where it's been stored, three classes to hold that data in an
# easily accessible form, and a bunch of functions to calculate stuff
# from data stored in instances of those classes. At the end of the
# file, there's a function called 'demonstrate' that shows what a few
# of these do.

from sqlite3 import connect
import get_soundcloud_data as gsc

db_path = 'scdb.sqlite'

#def get_table(tableName):
#    '''Returns a list of the contents of one entire table from the sqlite database.'''
#    try:
#        conn = connect(db_path)
#        with conn:
#            curs = conn.cursor()
#            curs.execute("SELECT * FROM {!s}".format(tableName))
#            return curs.fetchall()
#    except Exception:
#        # for some reason, table contents couldn't be retrieved
#        # Just return an empty list instead of a list of contents
#        return list()
        
class data_holder():
    'An object to hold data from each of the four tables in the database.'

    def __init__(self):
        # users = set of SoundCloud user objects
        self.users = gsc.get_table('users')
        # tracks = set of SoundCloud track objects which users in "users" have interacted with
        self.tracks = gsc.get_table('tracks')
        # x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "users")
        self.x_follows_y = gsc.get_table('x_follows_y')
        # favourites (NB UK spelling here, US spelling on SoundCloud) 
        #    - set of tuples representing tracks that a user has 'liked'
        self.favourites = gsc.get_table('favourites')
        # groups - set of tuples representing SoundCloud groups that a user has joined
        self.groups = gsc.get_table('groups')
        # comments - set of SoundCloud comments for a particular track
        self.comments = gsc.get_table('comments')
        # playlists - set of SoundCloud users' playlisted tracks
        self.playlists = gsc.get_table('playlists')
        
        

class entity_holder():
    'An object to hold data cheaply processed from those held in the above.'

    def __init__(self, data):
        self.users = {x[0] for x in data.users}
#        self.users = {x[0] for x in data.users if len(x[0]) != 10}
#        self.nonusers = {x[0] for x in data.users if len(x[0]) == 10}
        self.producers = {x[1] for x in data.tracks}
#        self.tracks = {x[0] for x in data.tracks}
#        self.receivers = {x[0] for x in data.x_follows_y}
#        self.received = {x[1] for x in data.x_follows_y}
#        self.rated = {x[1] for x in data.x_follows_y if x[2] >= 1}
#        self.raters = {x[0] for x in data.x_follows_y if x[2] >= 1}
#        self.recognitions = {x[:2] for x in data.x_follows_y # for self.followers 
#                             if x[2] >= rating_threshold}
#        self.highrated = {x[1] for x in self.recognitions}
#        self.followed = {x[0] for x in data.authorings 
#                           if x[1] in self.highrated}
        self.followed = {x[1] for x in data.x_follows_y}
        self.followers = {x[0] for x in data.x_follows_y}
#        self.author_users = self.producers & self.users
#        self.author_receivers = self.producers & self.receivers
#        self.author_raters = self.producers & self.raters
#        self.author_recognisers = self.producers & self.followers
#        self.recognised_recognisers = self.followed & self.followers
#        self.active_users = self.author_users | self.receivers


def printData(data):
    print('data.users (max 10, selected at random from '+str(len(data.users))+' users)')
    temp_copy = data.users.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user '+str(popped[0])+' '+popped[2])
        count = count+1
    
    print ''
    print('data.x_follows_y relationships (max 10 selected at random from '+str(len(data.x_follows_y))+' follow relationships)')
    temp_copy = data.x_follows_y.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1
        
    print ''
    print('data.tracks (max 10 selected at random from '+str(len(data.tracks))+' tracks)')
    temp_copy = data.tracks.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        try:  # might throw a type error if there are strange characters in the title or genre for a track
            print(str(count)+'. user id: '+str(popped[1])+', track id: '+str(popped[0])+', title: '+popped[9]+', genre: '+popped[31])
        except Exception:
            try:
                print(str(count)+'. user id: '+str(popped[1])+', track id: '+str(popped[0])+', title: '+str(unicode(popped[9].encode('utf-8')))+', genre: '+str(unicode(popped[31]).encode('utf-8')))
            except Exception as e2:
                print(str(count)+'. user id: '+str(popped[1])+', track id: '+str(popped[0])+', title and genre - error in displaying, '+ e2.message)
        count = count+1


def printEntities(entities):
    print ''
    print('entities.users - max 10 selected at random from total of '+str(len(entities.users)))
    temp_copy = entities.users.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped))
        count = count+1
    
    print ''
    print('entities.producers (max 10 selected at random from total of '+str(len(entities.producers)))
    temp_copy = entities.producers.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped))
        count = count+1

    print ''
    print('entities.followers (max 10 selected at random from total of '+str(len(entities.followers)))
    temp_copy = entities.followers.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped))
        count = count+1

    print ''
    print('entities.followed (max 10 selected at random from total of '+str(len(entities.followed)))
    temp_copy = entities.followed.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped))
        count = count+1



def getUserName(userId,data_users):
    '''Returns the human-readable name associated with an ID of a user.'''

    for u in data_users:
        if (u[0]==userId):
            return u[2]


def followers_of_user(user,data):
    '''Returns set of users who follow a given user'''

    followers = set([])
    for follow in data.x_follows_y:
        if (follow[1]==user):
            followers = followers | follow[0]
    return followers


#def demonstrate():
#    'This is just to show how things work.'
#
#    data = data_holder()
#    entities = entity_holder(data)
#    attributes = attribute_holder(data)
#
