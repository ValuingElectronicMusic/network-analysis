'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud
#Set up soundcloud API
import clientSettings as client
client = soundcloud.Client(client_id=client.get_client_id())
import sqlite3
import time
timeDelay = 0.05

# The following global variables represent information about the SoundCloud users in our
# sample set. We only collect data on users in our sample set, discarding other data  
# users = set of SoundCloud user objects
users = set()
# x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "users")
x_follows_y = set()
# tracks = set of SoundCloud track objects where tracks belong to users in "users"
tracks = set()
# TODO add the four items below as DB tables
# groups - set of SoundCloud groups that a user has joined
groups = set()
# favourites (NB English spelling here, US spelling on SoundCloud) 
#    - tracks that a user has 'liked'
favourites = set()
# comments - set of SoundCloud comments for a particular track
comments = set()


def printData():
    global users
    print('users (max 10, selected at random from '+str(len(users))+' users)')
    temp_copy = users.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user '+str(popped.id)+' '+popped.username)
        count = count+1
    
    global x_follows_y
    print ''
    print('X-follows-Y relationships (max 10 selected at random from '+str(len(x_follows_y))+' follow relationships)')
    temp_copy = x_follows_y.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1
        
    global tracks
    print ''
    print('tracks (max 10 selected at random from '+str(len(tracks))+' tracks)')
    temp_copy = tracks.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        try:  # might throw a type error if there are strange characters in the title or genre for a track
            print(str(count)+'. user id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title: '+popped.title+', genre: '+popped.genre)
        except Exception as e:
            print(str(count)+'. user id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title and genre - error in displaying, '+ e.message)
        count = count+1
            
        
def getRandomUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception as e:
            pass
        else:
            userfound = True    
    return user


def getXUserIDs(limit=10):
    users = set()
    for i in range(0,limit):
        #print i
        users.add(getRandomUser().id)
    return users


def getAllFollowers(user):
    strUserID = str(user.id)
    followers = client.get('/users/'+strUserID+'/followers')
    print('Exploring followers of User = '+ strUserID+' with '+str(len(followers))+' followers')
    return followers


def getAllFollowings(user):
    strUserID = str(user.id)
    followings = client.get('/users/'+strUserID+'/followings')
    print('Exploring following activities of User = '+ strUserID+' who follows '+str(len(followings))+' users')
    return followings


def getNewSnowballSample(sampleSize=10):
    ''' Generates a new sample of users (set to the specified sample size, default 10), also generating 
    data on those users' tracks and follow relationships between the users in the set 
    N.B. This wipes any previously collected samples that are only stored in local memory '''
    
    global users
    global tracks
    global x_follows_y
    global groups
    global favourites
    users = set() # initialised to empty
    x_follows_y = set() # initialised to empty
    tracks = set() # initialised to empty
    groups = set() # initialised to empty
    favourites = set() # initialised to empty
    comments = set() # initialised to empty
    print('Generating snowball sample with a sample size of '+str(sampleSize))
    while (len(users)<sampleSize):
        user = getRandomUser() # get a new starting point at random        
        if (not(user in users)):
            users.add(user)
        print('Seed user = '+str(user.id))
        if (len(users)<sampleSize):  #in case adding the new user to our sample brings us to our desired samplesize
            collectUsersFromSeedUser(user,sampleSize)
     # populate the contents of the remaining global variables  with data relating to the new sample of users
    getTracks()
    getFavourites()
    getGroups()
    #getPlaylists()
    getComments()

def collectUsersFromSeedUser(user,sampleSize):
    ''' Populate the users and x_follows_y sets with data sampled from SoundCloud '''
    global users
    global x_follows_y
    # look for all followers of user    
    followers = getAllFollowers(user)
    # add each follower to users set
    count=0
    while (len(users)<sampleSize and count<len(followers)): # repeat till sample size reached
        print('length = '+str(len(users))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followers = '+str(len(followers)))
        print('user '+str(followers[count].id)+' follows '+str(user.id))
        # Add the follower to the set of SC users
        if (not(followers[count] in users)):
            users.add(followers[count]) 
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((followers[count].id, user.id))
        count = count+1
      
    # look for all followings of user (i.e. all users that our seed user follows)    
    followings = getAllFollowings(user)
    # add each follower to users set
    count=0
    while (len(users)<sampleSize and count<len(followings)): # repeat till sample size reached
        print('length = '+str(len(users))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followings = '+str(len(followings)))
        print('user '+str(user.id)+' follows '+str(followings[count].id))
        # Add the follower to the set of SC users
        if (not(followings[count] in users)):       
            users.add(followings[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
        # Add follows relationships between the seed user and the user they follow
        x_follows_y.add((user.id, followings[count].id))
        count = count+1
        
    # repeat this step with each follower as the seed user, picking up the results in users
    time.sleep(timeDelay)
    count = 0
    while (len(users)<sampleSize and count<len(followers)):
        collectUsersFromSeedUser(followers[count],sampleSize)
        time.sleep(timeDelay)
        count = count+1
        
    # repeat this step with each following (user that the seed user follows) as the seed user, picking up the results in users
    count = 0
    while (len(users)<sampleSize and count<len(followings)):
        collectUsersFromSeedUser(followings[count],sampleSize)
        time.sleep(timeDelay)
        count = count+1


def getTracks():
    print 'Getting data about users\' tracks...'
    global users
    global tracks
    for user in users:
        u_id = user.id 
        user_tracks = client.get('/users/'+str(u_id)+'/tracks')
        for u_track in user_tracks:
            if (not(u_track in tracks)):
                tracks.add(u_track)
        time.sleep(timeDelay)
    
def getGroups():
    print 'Getting data about users\' groups...'
    global users
    global groups
    for user in users:
        u_id = user.id 
        user_groups = client.get('/users/'+str(u_id)+'/groups')
        for u_group in user_groups:
            if (not(u_group in groups)):
                groups.add((u_id, u_group.id))
        time.sleep(timeDelay)


        
def getFavourites():
    print 'Getting data about users\' likes...'
    global users
    global favourites
    for user in users:
        u_id = user.id 
        user_favourites = client.get('/users/'+str(u_id)+'/favorites') # Note US spelling
        for u_favourite in user_favourites:
            favourites.add((u_id, u_favourite.id))
        time.sleep(timeDelay)
    
    
#def getPlaylists():
#    print 'Getting data about users\' playlists...'
#    global users
#    global playlists
#    for user in users:
#        u_id = user.id 
#        user_playlists = client.get('/users/'+str(u_id)+'/playlists') 
#        for u_playlist in user_playlists:
#            for u_track in u_playlist.tracks
#                playlists.add((u_id, u_playlist.id, u_track.id))
#        time.sleep(timeDelay)    
    
    
def getComments():
    print 'Getting data about comments on users\' tracks...'
    global users
    global comments
    for user in users:
        u_id = user.id 
        user_comments = client.get('/users/'+str(u_id)+'/comments')
        for u_comment in user_comments:
            comments.add(u_comment)
        time.sleep(timeDelay)
    

def exportDataToSQLite():
    global users
    global x_follows_y
    global tracks
    dbFileName='scdb.sqlite'
    try:
        db = sqlite3.connect(dbFileName)
        cursor = db.cursor()
        # Start with fresh database
        cursor.execute('''DROP TABLE IF EXISTS users''')
        cursor.execute('''DROP TABLE IF EXISTS x_follows_y''')
        cursor.execute('''DROP TABLE IF EXISTS tracks''')
        cursor.execute('''DROP TABLE IF EXISTS groups''')
        cursor.execute('''DROP TABLE IF EXISTS favourites''')
        cursor.execute('''DROP TABLE IF EXISTS comments''')
        db.commit()
        print 'Creating users table in DB....'
        # Check if table users does not exist and create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, permalink TEXT, username TEXT, uri TEXT,
                             permalink_url TEXT, avatar_url TEXT, country TEXT, full_name TEXT, 
                             city TEXT, description TEXT, discogs_name TEXT, myspace_name TEXT,
                             website TEXT, website_title TEXT, online TEXT, track_count INTEGER,
                             playlist_count INTEGER, followers_count INTEGER, 
                             followings_count INTEGER, public_favorites_count INTEGER)''')
        print('Adding data to users table in DB.... Total num of users: '+str(len(users)))
        for user in users:
#            print('Inserting user '+str(user.id)+' into the database. Total num of users: '+str(len(users)))
            # USERS table: fields, description and example value:
            #id     integer ID     123
            #permalink     permalink of the resource     "sbahn-sounds"
            #username     username     "Doctor Wilson"
            #uri     API resource URL     http://api.soundcloud.com/comments/32562
            #permalink_url     URL to the SoundCloud.com page     "http://soundcloud.com/bryan/sbahn-sounds"
            #avatar_url     URL to a JPEG image     "http://i1.sndcdn.com/avatars-000011353294-n0axp1-large.jpg"
            #country     country     "Germany"
            #full_name     first and last name     "Tom Wilson"
            #city     city     "Berlin"
            #description     description     "Buskers playing in the S-Bahn station in Berlin"
            #discogs-name     Discogs name     "myrandomband"
            #myspace-name     MySpace name     "myrandomband"
            #website     a URL to the website     "http://facebook.com/myrandomband"
            #website-title     a custom title for the website     "myrandomband on Facebook"
            #online     online status (boolean)     true
            #track_count     number of public tracks     4
            #playlist_count     number of public playlists     5
            #followers_count     number of followers     54
            #followings_count     number of followed users     75
            #public_favorites_count     number of favorited public tracks     7
            #avatar_data     binary data of user avatar     (only for uploading)
            try:
                cursor.execute('''INSERT INTO users(id, username,
                             permalink_url, full_name, description,  
                             city, country,
                             track_count, playlist_count, 
                             followers_count, followings_count, public_favorites_count) 
                             VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                             (user.id, user.username, 
                              user.permalink_url, user.full_name, user.description, 
                              user.city, user.country, 
                              user.track_count, user.playlist_count, 
                              user.followers_count, user.followings_count, user.public_favorites_count))
            except Exception as e:
                print('Error adding user '+str(user.id)+' to the database: '+e.message+' '+str(e.args))
        # X FOLLOWS Y set of tuples (follower.id, followed.id) 
        print 'Creating x_follows_y table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS x_follows_y(follower INTEGER, followed INTEGER, PRIMARY KEY (follower, followed))''')
        print('Adding data to x_follows_y table in DB.... Total num of follows_rels: '+str(len(x_follows_y)))
        for follow in x_follows_y:
#            print('Inserting '+str(follow[0])+' follows '+str(follow[1])+' into the database. Total num of follows_rels: '+str(len(x_follows_y)))
            try:
                cursor.execute('''INSERT INTO x_follows_y(follower, followed) 
                              VALUES(?, ?)''', 
                              (follow[0], follow[1]))
            except Exception as e:
                print('Error adding ['+str(follow[0])+' follows '+str(follow[1])+'] to the database: '+e.message+' '+str(e.args))
        # TRACKS
#        attachments_uri
#        video_url
#        track_type
#        release_month
#        original_format
#        label_name
#        duration
#        id
#        streamable
#        user_id
#        title
#        favoritings_count
#        commentable
#        label_id
#        state
#        downloadable
#        waveform_url
#        sharing
#        description
#        release_day
#        purchase_url
#        permalink
#        purchase_title
#        stream_url
#        key_signature
#        user
#        genre
#        isrc
#        download_count
#        permalink_url
#        playback_count
#        kind
#        release_year
#        license
#        artwork_url
#        created_at
#        bpm
#        uri
#        original_content_size
#        comment_count
#        release
#        tag_list
#        embeddable_by

        print 'Creating tracks table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,   
        permalink_url TEXT,  track_type TEXT, state TEXT, created_at TEXT, 
        original_format TEXT, description TEXT, sharing TEXT,   
        genre TEXT, duration INTEGER, key_signature TEXT, bpm INTEGER, 
        license TEXT, label_id INTEGER, label_name TEXT,
        playback_count INTEGER,  
        favoritings_count INTEGER, 
        streamable TEXT, stream_url TEXT, 
        downloadable TEXT, download_count INTEGER, 
        commentable TEXT, comment_count INTEGER,
        purchase_url TEXT, artwork_url TEXT, video_url TEXT, embeddable_by TEXT,
        release TEXT, release_month INTEGER, release_day INTEGER, release_year INTEGER,  
        tag_list TEXT)''')   
        print('Adding data to tracks table in DB..... Total num of tracks: '+str(len(tracks)))
        for track in tracks:
            try:
                cursor.execute('''INSERT INTO tracks(id, user_id, title,   
        permalink_url,  track_type, state, created_at, 
        original_format, description, sharing,   
        genre, duration, key_signature, bpm, 
        license, label_id, label_name,
        playback_count,  
        favoritings_count, 
        streamable, stream_url, 
        downloadable, download_count, 
        commentable, comment_count,
        purchase_url, artwork_url, video_url, embeddable_by,
        release, release_month, release_day, release_year,  
        tag_list) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?, ?, ?, ?)''',
                {track.id, track.user_id, track.title,   
                track.permalink_url, track.track_type, track.state, track.created_at, 
                track.original_format, track.description, track.sharing,   
                track.genre, track.duration, track.key_signature, track.bpm, 
                track.license, track.label_id, track.label_name,
                track.playback_count,  
                track.favoritings_count, 
                track.streamable, track.stream_url, 
                track.downloadable, track.download_count, 
                track.commentable, track.comment_count,
                track.purchase_url, track.artwork_url, track.video_url, track.embeddable_by,
                track.release, track.release_month, track.release_day, track.release_year,  
                track.tag_list}) 
            except Exception as e:
                print('Error adding track '+str(track.id)+' to the database: '+e.message+' '+str(e.args))
        # GROUPS information about what groups users belong to 
        print 'Creating groups table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups(user_id INTEGER, group_id INTEGER, PRIMARY KEY (user_id, group_id))''')
        print('Adding data to groups table in DB.... Total num of group memberships: '+str(len(groups)))
        for group in groups:
            try:
                cursor.execute('''INSERT INTO groups(user_id, group_id) 
                              VALUES(?, ?)''', 
                              (group[0], group[1]))
            except Exception as e:
                print('Error adding user '+str(group[0])+' group membership of '+str(group[1])+' to the database: '+e.message+' '+str(e.args))
        # PLAYLISTS information about what tracks users add to playlists 
        # leave this for now
        
        # FAVOURITES information about what tracks a user Likes
        print 'Creating favourites table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS favourites(user INTEGER, track INTEGER, PRIMARY KEY (user, track))''')
        print('Adding data to favourites table in DB.... Total num of favourite entries: '+str(len(favourites)))
        for favourite in favourites:
            try:
                cursor.execute('''INSERT INTO favourites(user, track) 
                              VALUES(?, ?)''', 
                              (favourite[0], favourite[1]))
            except Exception as e:
                print('Error adding user '+str(favourite[0])+' favouriting track '+str(favourite[1])+' to the database: '+e.message+' '+str(e.args))
        # COMMENTS information about what comments a user makes on tracks
        # (restricted to the tracks produced by users in the sample)
        print 'Creating comments table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments(id INTEGER PRIMARY KEY,
        body TEXT, user_id INTEGER, track_id INTEGER, 
        timestamp INTEGER, created_at TEXT)''')
        print('Adding data to comments table in DB.... Total num of comment entries: '+str(len(comments)))
        for comment in comments:
            try:
                cursor.execute('''INSERT INTO comments(id, body, user_id, track_id, timestamp, created_at) 
                              VALUES(?, ?, ?, ?, ?, ?)''', 
                              (comment.id, comment.body, comment.user_id, comment.track_id, 
                               comment.timestamp, comment.created_at))
            except Exception as e:
                print('Error adding user comment '+str(comment.id)+' to the database: '+e.message+' '+str(e.args))
        print 'Ready to commit DB to file'
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        print 'Exception caught in exportDataToSQLite function'
        print e.message
        print(str(e.args))
        #raise e
    finally:
        # Close the db connection
        db.close()
        print('Data saved in '+dbFileName)

def main(sampleSize = 15): 
    getNewSnowballSample(sampleSize)
    printData() 
    exportDataToSQLite()