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
timeDelay = 0.5

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
# playlists - set of [groups of tracks] that a user has added to a playlist
playlists = set()
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
    global playlists
    global favourites
    users = set() # initialised to empty
    x_follows_y = set() # initialised to empty
    tracks = set() # initialised to empty
    groups = set() # initialised to empty
    playlists = set() # initialised to empty
    favourites = set() # initialised to empty
    comments = set() # initialised to empty
    print('Generating snowball sample with a sample size of '+str(sampleSize))
    while (len(users)<sampleSize):
        user = getRandomUser() # get a new starting point at random        
        users.add(user)
        print('Seed user = '+str(user.id))
        if (len(users)<sampleSize):  #in case adding the new user to our sample brings us to our desired samplesize
            collectUsersFromSeedUser(user,sampleSize)
     # populate the contents of the remaining global variables  with data relating to the new sample of users
    getTracks()
    getGroups()
    getPlaylists()
    getFavourites()
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
        users.add(followers[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
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
            groups.add(u_group)
        time.sleep(timeDelay)

def getPlaylists():
    print 'Getting data about users\' playlists...'
    global users
    global playlists
    for user in users:
        u_id = user.id 
        user_playlists = client.get('/users/'+str(u_id)+'/playlists')
        for u_playlist in user_playlists:
            playlists.add(u_playlist)
        time.sleep(timeDelay)
    
        
def getFavourites():
    print 'Getting data about users\' likes...'
    global users
    global favourites
    for user in users:
        u_id = user.id 
        user_favourites = client.get('/users/'+str(u_id)+'/favorites') # Note US spelling
        for u_favourite in user_favourites:
            favourites.add(u_favourite)
        time.sleep(timeDelay)
    
    
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
        cursor.execute('''DROP TABLE IF EXISTS playlists''')
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
            cursor.execute('''INSERT INTO users(id, permalink, username, uri,
                             permalink_url, avatar_url, country, full_name, 
                             city, description, discogs_name, myspace_name,
                             website, website_title, online, track_count,
                             playlist_count, followers_count, 
                             followings_count, public_favorites_count) 
                             VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                             (user.id, user.permalink, user.username, user.uri, user.permalink_url, 
                              user.avatar_url, user.country, user.full_name, user.city, 
                              user.description, user.discogs_name, user.myspace_name, user.website, 
                              user.website_title, user.online, user.track_count, user.playlist_count, 
                              user.followers_count, user.followings_count, user.public_favorites_count))

        # X FOLLOWS Y set of tuples (follower.id, followed.id) 
        print 'Creating x_follows_y table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS x_follows_y(follower INTEGER, followed INTEGER, PRIMARY KEY (follower, followed))''')
        print('Adding data to x_follows_y table in DB.... Total num of follows_rels: '+str(len(x_follows_y)))
        for follow in x_follows_y:
#            print('Inserting '+str(follow[0])+' follows '+str(follow[1])+' into the database. Total num of follows_rels: '+str(len(x_follows_y)))
            cursor.execute('''INSERT INTO x_follows_y(follower, followed) 
                              VALUES(?, ?)''', 
                              (follow[0], follow[1]))
        # TRACKS
        #id     integer ID     123
        #created_at     timestamp of creation     "2009/08/13 18:30:10 +0000"
        #user_id     user-id of the owner     343
        #user     mini user representation of the owner     {id: 343, username: "Doctor Wilson"...}
        #title     track title     "S-Bahn Sounds"
        #permalink     permalink of the resource     "sbahn-sounds"
        #permalink_url     URL to the SoundCloud.com page     "http://soundcloud.com/bryan/sbahn-sounds"
        #uri     API resource URL     "http://api.soundcloud.com/tracks/123"
        #sharing     public/private sharing     "public"
        #embeddable_by     who can embed this track or playlist     "all", "me", or "none"
        #purchase_url     external purchase link     "http://amazon.com/buy/a43aj0b03"
        #artwork_url     URL to a JPEG image     "http://i1.sndcdn.com/a....-large.jpg?142a848"
        #description     HTML description     "my first track"
        #label     label mini user object     {id:123, username: "BeatLabel"...}
        #duration     duration in milliseconds     1203400
        #genre     genre     "HipHop"
        #shared_to_count     number of sharings (if private)     45
        #tag_list     list of tags     "tag1 \"hip hop\" geo:lat=32.444 geo:lon=55.33"
        #label_id     id of the label user     54677
        #label_name     label name     "BeatLabel"
        #release     release number     3234
        #release_day     day of the release     21
        #release_month     month of the release     5
        #release_year     year of the release     2001
        #streamable     streamable via API (boolean)     true
        #downloadable     downloadable (boolean)     true
        #state     encoding state     "finished"
        #license     creative common license     "no-rights-reserved"
        #track_type     track type     "recording"
        #waveform_url     URL to PNG waveform image     "http://w1.sndcdn.com/fxguEjG4ax6B_m.png"
        #download_url     URL to original file     "http://api.soundcloud.com/tracks/3/download"
        #stream_url     link to 128kbs mp3 stream     "http://api.soundcloud.com/tracks/3/stream"
        #video_url     a link to a video page     "http://vimeo.com/3302330"
        #bpm     beats per minute     120
        #commentable     track commentable (boolean)     true
        #isrc     track ISRC     "I123-545454"
        #key_signature     track key     "Cmaj"
        #comment_count     track comment count     12
        #download_count     track download count     45
        #playback_count     track play count     435
        #favoritings_count     track favoriting count     6
        #original_format     file format of the original file     "aiff"
        #original_content_size     size in bytes of the original file     10211857
        #created_with     the app that the track created     {"id"=>3434, "..."=>nil}
        ####asset_data     binary data of the audio file     (only for uploading)
        ####artwork_data     binary data of the artwork image     (only for uploading)
        #user_favorite     track favorite of current user (boolean, authenticated requests only)
        print 'Creating tracks table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, 
        video_url TEXT, track_type TEXT, release_month INTEGER, original_format TEXT, label_name TEXT, duration INTEGER, streamable TEXT, user_id INTEGER, title TEXT, favoritings_count INTEGER, commentable TEXT, label_id TEXT, state TEXT, downloadable TEXT, waveform_url TEXT, sharing TEXT, description TEXT, release_day INTEGER, purchase_url TEXT, permalink TEXT, purchase_title TEXT, stream_url TEXT, key_signature TEXT, user_username TEXT, user_permalink TEXT, user_kind TEXT, user_uri TEXT, user_avatar_url TEXT, user_permalink_url TEXT, user_id_dup INTEGER, genre TEXT, isrc TEXT, download_count INTEGER, permalink_url TEXT, playback_count INTEGER, kind TEXT, release_year INTEGER, license TEXT, artwork_url TEXT, created_at TEXT, bpm INTEGER, uri TEXT, original_content_size INTEGER, comment_count INTEGER, release TEXT, tag_list TEXT, embeddable_by TEXT)''')   
        print('Adding data to tracks table in DB..... Total num of tracks: '+str(len(tracks)))
        for track in tracks:
#            print('Inserting track '+str(track.id)+' into the database. Total num of tracks: '+str(len(tracks)))
#            print('id'+str(track.id))
#            print(' video_url'+str(track.video_url))
#            print(' track_type'+str(track.track_type))
#            print(' release_month'+str(track.release_month)+' original_format'+str(track.original_format))
#            print(' label_name'+str(track.label_name)+' duration'+str(track.duration))
#            print(' streamable'+str(track.streamable)+' user_id'+str(track.user_id)+' title'+str(track.title))
#            print(' favoritings_count'+str(track.favoritings_count)+' commentable'+str(track.commentable))
#            print(' label_id'+str(track.label_id)+' state'+str(track.state))
#            print('downloadable'+str(track.downloadable)+' waveform_url'+str(track.waveform_url))
#            print(' sharing'+str(track.sharing)+' description'+str(track.description))
#            print(' release_day'+str(track.release_day)+' purchase_url'+str(track.purchase_url))
#            print(' permalink'+str(track.permalink)+' purchase_title'+str(track.purchase_title)+' stream_url'+str(track.stream_url))
#            print(' key_signature'+str(track.key_signature)+' user_username'+str(track.user['username']))
#            print(' user_permalink'+str(track.user['permalink'])+' user_kind'+str(track.user['kind']))
#            print(' user_uri'+str(track.user['uri'])+' user_avatar_url'+str(track.user['avatar_url']))
#            print(' user_permalink_url'+str(track.user['permalink_url'])+' user_id_dup'+str(track.user['id']))
#            print(' genre'+str(track.genre)+' isrc'+str(track.isrc)+' download_count'+str(track.download_count))
#            print(' permalink_url'+str(track.permalink_url)+' playback_count'+str(track.playback_count))
#            print(' kind'+str(track.kind)+' release_year'+str(track.release_year)+' license'+str(track.license))
#            print(' artwork_url'+str(track.artwork_url)+' created_at'+str(track.created_at)+' bpm'+str(track.bpm))
#            print(' uri'+str(track.uri)+' original_content_size'+str(track.original_content_size))
#            print(' comment_count'+str(track.comment_count)+' release'+str(track.release))
#            print(' tag_list'+str(track.tag_list))
#            print(' embeddable_by'+str(track.embeddable_by))
#            print('-------------------------------')
#            print('-------------------------------')
#            print('-------------------------------')
            cursor.execute('''INSERT INTO tracks(id, video_url, track_type, release_month, original_format, label_name, duration, streamable, user_id, title, favoritings_count, commentable, label_id, state, downloadable, waveform_url, sharing, description, release_day, purchase_url, permalink, purchase_title, stream_url, key_signature, user_username, user_permalink, user_kind, user_uri, user_avatar_url, user_permalink_url, user_id_dup, genre, isrc, download_count, permalink_url, playback_count, kind, release_year, license, artwork_url, created_at, bpm, uri, original_content_size, comment_count, release, tag_list, embeddable_by) 
            VALUES(:id, :video_url, :track_type, :release_month, :original_format, :label_name, :duration, :streamable, :user_id, :title, :favoritings_count, :commentable, :label_id, :state, :downloadable, :waveform_url, :sharing, :description, :release_day, :purchase_url, :permalink, :purchase_title, :stream_url, :key_signature, :user_username, :user_permalink, :user_kind, :user_uri, :user_avatar_url, :user_permalink_url, :user_id_dup, :genre, :isrc, :download_count, :permalink_url, :playback_count, :kind, :release_year, :license, :artwork_url, :created_at, :bpm, :uri, :original_content_size, :comment_count, :release, :tag_list, :embeddable_by)''',
            {'id': track.id, 'video_url': track.video_url, 'track_type': track.track_type, 'release_month': track.release_month, 'original_format': track.original_format, 'label_name': track.label_name, 'duration': track.duration, 'streamable': track.streamable, 'user_id': track.user_id, 'title': track.title, 'favoritings_count': track.favoritings_count, 'commentable': track.commentable, 'label_id': track.label_id, 'state': track.state, 'downloadable': track.downloadable, 'waveform_url': track.waveform_url, 'sharing': track.sharing, 'description': track.description, 'release_day': track.release_day, 'purchase_url': track.purchase_url, 'permalink': track.permalink, 'purchase_title': track.purchase_title, 'stream_url': track.stream_url, 'key_signature': track.key_signature, 'user_username': track.user['username'], 'user_permalink': track.user['permalink'], 'user_kind': track.user['kind'], 'user_uri': track.user['uri'], 'user_avatar_url': track.user['avatar_url'], 'user_permalink_url': track.user['permalink_url'], 'user_id_dup': track.user['id'], 'genre': track.genre, 'isrc': track.isrc, 'download_count': track.download_count, 'permalink_url': track.permalink_url, 'playback_count': track.playback_count, 'kind': track.kind, 'release_year': track.release_year, 'license': track.license, 'artwork_url': track.artwork_url, 'created_at': track.created_at, 'bpm': track.bpm, 'uri': track.uri, 'original_content_size': track.original_content_size, 'comment_count': track.comment_count, 'release': track.release, 'tag_list': track.tag_list, 'embeddable_by': track.embeddable_by}) 
#    {u'attachments_uri': u'https://api.soundcloud.com/tracks/101369139/attachments', u'video_url': None, u'track_type': None, u'release_month': None, u'original_format': u'mp3', u'label_name': None, u'duration': 310128, u'id': 101369139, u'streamable': True, u'user_id': 50716341, u'title': u'Mc Daleste Angra Dos Reis', u'favoritings_count': 0, u'commentable': True, u'label_id': None, u'state': u'finished', u'downloadable': False, u'waveform_url': u'https://w1.sndcdn.com/9ssVt2Lko43R_m.png', u'sharing': u'public', u'description': u'', u'release_day': None, u'purchase_url': None, u'permalink': u'mc-daleste-angra-dos-reis', u'purchase_title': None, u'stream_url': u'https://api.soundcloud.com/tracks/101369139/stream', u'key_signature': None, u'user': {u'username': u'Arthur Brandalise', u'permalink': u'arthur-brandalise', u'kind': u'user', u'uri': u'https://api.soundcloud.com/users/50716341', u'avatar_url': u'https://i1.sndcdn.com/avatars-000047085500-obeiji-large.jpg?435a760', u'permalink_url': u'http://soundcloud.com/arthur-brandalise', u'id': 50716341}, u'genre': u'Funk', u'isrc': None, u'download_count': 0, u'permalink_url': u'http://soundcloud.com/arthur-brandalise/mc-daleste-angra-dos-reis', u'playback_count': 73, u'kind': u'track', u'release_year': None, u'license': u'all-rights-reserved', u'artwork_url': None, u'created_at': u'2013/07/17 02:11:32 +0000', u'bpm': None, u'uri': u'https://api.soundcloud.com/tracks/101369139', u'original_content_size': 7712965, u'comment_count': 0, u'release': None, u'tag_list': u'', u'embeddable_by': u'all'}
        # GROUPS information about what groups users belong to 
        print 'Creating groups table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS groups(id INTEGER, user INTEGER, PRIMARY KEY (id, user))''')
        print('Adding data to groups table in DB.... Total num of group memberships: '+str(len(groups)))
        for group in groups:
            cursor.execute('''INSERT INTO groups(id, user) 
                              VALUES(?, ?)''', 
                              (group[0], group[1]))
        # PLAYLISTS information about what tracks users add to playlists 
        print 'Creating playlists table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS playlists(id INTEGER, user INTEGER, track INTEGER, PRIMARY KEY (id, user, track))''')
        print('Adding data to playlists table in DB.... Total num of playlist entries: '+str(len(playlists)))
        for playlist in playlists:
            cursor.execute('''INSERT INTO playlists(id, user, track) 
                              VALUES(?, ?, ?)''', 
                              (playlist[0], playlist[1], playlist[2]))
        # FAVOURITES information about what tracks a user Likes
        print 'Creating favourites table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS favourites(user INTEGER, track INTEGER, PRIMARY KEY (user, track))''')
        print('Adding data to favourites table in DB.... Total num of favourite entries: '+str(len(favourites)))
        for favourite in favourites:
            cursor.execute('''INSERT INTO favourites(user, track) 
                              VALUES(?, ?)''', 
                              (favourite[0], favourite[1]))
        # COMMENTS information about what comments a user makes on tracks
        # (restricted to the tracks produced by users in the sample)
        print 'Creating comments table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS comments(id INTEGER PRIMARY KEY, track INTEGER, user INTEGER, content TEXT''')
        print('Adding data to comments table in DB.... Total num of comment entries: '+str(len(comments)))
        for comment in comments:
            cursor.execute('''INSERT INTO comments(id, track, user, content) 
                              VALUES(?, ?, ?, ?)''', 
                              (comment[0], comment[1], comment[2], comment[3]))

        print 'Ready to commit DB to file'
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        print 'Exception caught'
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