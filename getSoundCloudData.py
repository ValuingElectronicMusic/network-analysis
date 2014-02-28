'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud
#Set up soundcloud API
import clientSettings as client
client = soundcloud.Client(client_id=client.get_client_id())
import sqlite


# agents = set of SoundCloud user objects
agents = set()
# x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "agents")
x_follows_y = set()
# tracks = set of SoundCloud track objects where tracks belong to users in "agents"
tracks = set()



def printData():
    global agents
    print('agents (max 10, selected at random from '+str(len(agents))+' agents)')
    temp_copy = agents.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent '+str(popped.id)+' '+popped.username)
        count = count+1
    
    global x_follows_y
    print ''
    print('X-follows-Y relationships (max 10 selected at random from '+str(len(x_follows_y))+' follow relationships)')
    temp_copy = x_follows_y.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1
        
    global tracks
    print ''
    print('tracks (max 10 selected at random from '+str(len(tracks))+' tracks)')
    temp_copy = tracks.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        try:  # might throw a type error if there are strange characters in the title or genre for a track
            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title: '+popped.title+', genre: '+popped.genre)
        except Exception as e:
            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title and genre - error in displaying, '+ e.message)
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
    
    global agents
    global tracks
    global x_follows_y
    agents = set() # initialised to empty
    x_follows_y = set() # initialised to empty
    tracks = set() # initialised to empty
    
    print('Generating snowball sample with a sample size of '+str(sampleSize))
    while (len(agents)<sampleSize):
        user = getRandomUser() # get a new starting point at random        
        agents.add(user)
        print('Seed user = '+str(user.id))
        if (len(agents)<sampleSize):  #in case adding the new user to our sample brings us to our desired samplesize
            collectUsersFromSeedUser(user,sampleSize)
    
    tracks = getTracks() # populate the contents of the global "tracks" set  with tracks relating to the new sample of users
    

def collectUsersFromSeedUser(user,sampleSize):
    ''' Populate the agents and x_follows_y sets with data sampled from SoundCloud '''
    global agents
    global x_follows_y
    # look for all followers of user    
    followers = getAllFollowers(user)
    # add each follower to agents set
    count=0
    while (len(agents)<sampleSize and count<len(followers)): # repeat till sample size reached
        print('length = '+str(len(agents))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followers = '+str(len(followers)))
        print('user '+str(followers[count].id)+' follows '+str(user.id))
        # Add the follower to the set of SC agents
        agents.add(followers[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((followers[count].id, user.id))
        count = count+1
      
    # look for all followings of user    
    followings = getAllFollowings(user)
    # add each follower to agents set
    count=0
    while (len(agents)<sampleSize and count<len(followings)): # repeat till sample size reached
        print('length = '+str(len(agents))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followings = '+str(len(followings)))
        print('user '+str(user.id)+' follows '+str(followings[count].id))
        # Add the follower to the set of SC agents
        agents.add(followings[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
        # Add follows relationships between the seed user and the user they follow
        x_follows_y.add((user.id, followings[count].id))
        count = count+1
       
    # repeat this step with each follower as the seed user, picking up the results in agents
    count = 0
    while (len(agents)<sampleSize and count<len(followers)):
        collectUsersFromSeedUser(followers[count],sampleSize)
        count = count+1
        
    # repeat this step with each following (user that the seed user follows) as the seed user, picking up the results in agents
    count = 0
    while (len(agents)<sampleSize and count<len(followings)):
        collectUsersFromSeedUser(followings[count],sampleSize)
        count = count+1


def getTracks():
    global agents
    new_tracks = set()
    for agent in agents:
        a_id = agent.id 
        agent_tracks = client.get('/users/'+str(a_id)+'/tracks')
        for a_track in agent_tracks:
            new_tracks.add(a_track)
    return new_tracks

def exportDataToSQLite():
    global agents
    global x_follows_y
    global tracks
    dbFileName='scdb.sqlite'
    try:
        db = sqlite3.connect(dbFileName)
        cursor = db.cursor()
        # Check if table users does not exist and create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                      agents(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT unique, password TEXT)''')
        for agent in agents:
            cursor.execute('''INSERT INTO agents(id, permalink, username, uri, permalink_url, avatar_url, country, full_name, city, description, discogs_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (x.id, x.permalink, x.username, x.uri, x.permalink_url, x.avatar_url, x.country, x.full_name, x.city, x.description, x.discogs_name))
    #  Users  {
#  "id": 3207,
#  "permalink": "jwagener",
#  "username": "Johannes Wagener",
#  "uri": "http://api.soundcloud.com/users/3207",
#  "permalink_url": "http://soundcloud.com/jwagener",
#  "avatar_url": "http://i1.sndcdn.com/avatars-000001552142-pbw8yd-large.jpg?142a848",
#  "country": "Germany",
#  "full_name": "Johannes Wagener",
#  "city": "Berlin",
#  "description": "<b>Hacker at SoundCloud</b>\r\n\r\nSome of my recent Hacks:\r\n\r\nsoundiverse.com \r\nbrowse recordings with the FiRe app by artwork\r\n\r\ntopbillin.com \r\nfind people to follow on SoundCloud\r\n\r\nchatter.fm \r\nget your account hooked up with a voicebox\r\n\r\nrecbutton.com \r\nrecord straight to your soundcloud account",
#  "discogs_name": null,
#  "myspace_name": null,
#  "website": "http://johannes.wagener.cc",
#  "website_title": "johannes.wagener.cc",
#  "online": true,
#  "track_count": 12,
#  "playlist_count": 1,
#  "followers_count": 417,
#  "followings_count": 174,
#  "public_favorites_count": 26
#}
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

# x_follows_y set of tuples (follower.id, followed.id) 
        cursor.execute('''CREATE TABLE IF NOT EXISTS x_follows_y(id INTEGER PRIMARY KEY, name TEXT,
                                                                 phone TEXT, email TEXT unique, password TEXT)''')
        for follow in x_follows_y:
            cursor.execute('''INSERT INTO x_follows_y(id, permalink, username, uri, permalink_url, 
                              avatar_url, country, full_name, city, description, discogs_name) 
                              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                              (x.id, x.permalink, x.username, x.uri, x.permalink_url, x.avatar_url, 
                               x.country, x.full_name, x.city, x.description, x.discogs_name))
# TRACKS
        cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(id INTEGER PRIMARY KEY, name TEXT, 
        phone TEXT, email TEXT unique, password TEXT)''')
        for track in tracks:
            cursor.execute('''INSERT INTO agents(id, permalink, username, uri, permalink_url, avatar_url, 
            country, full_name, city, description, discogs_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (x.id, x.permalink, x.username, x.uri, x.permalink_url, x.avatar_url, x.country, 
             x.full_name, x.city, x.description, x.discogs_name))
#{
#  "id": 13158665,
#  "created_at": "2011/04/06 15:37:43 +0000",
#  "user_id": 3699101,
#  "duration": 18109,
#  "commentable": true,
#  "state": "finished",
#  "sharing": "public",
#  "tag_list": "soundcloud:source=iphone-record",
#  "permalink": "munching-at-tiannas-house",
#  "description": null,
#  "streamable": true,
#  "downloadable": true,
#  "genre": null,
#  "release": null,
#  "purchase_url": null,
#  "label_id": null,
#  "label_name": null,
#  "isrc": null,
#  "video_url": null,
#  "track_type": "recording",
#  "key_signature": null,
#  "bpm": null,
#  "title": "Munching at Tiannas house",
#  "release_year": null,
#  "release_month": null,
#  "release_day": null,
#  "original_format": "m4a",
#  "original_content_size": 10211857,
#  "license": "all-rights-reserved",
#  "uri": "http://api.soundcloud.com/tracks/13158665",
#  "permalink_url": "http://soundcloud.com/user2835985/munching-at-tiannas-house",
#  "artwork_url": null,
#  "waveform_url": "http://w1.sndcdn.com/fxguEjG4ax6B_m.png",
#  "user": {
#    "id": 3699101,
#    "permalink": "user2835985",
#    "username": "user2835985",
#    "uri": "http://api.soundcloud.com/users/3699101",
#    "permalink_url": "http://soundcloud.com/user2835985",
#    "avatar_url": "http://a1.sndcdn.com/images/default_avatar_large.png?142a848"
#  },
#  "stream_url": "http://api.soundcloud.com/tracks/13158665/stream",
#  "download_url": "http://api.soundcloud.com/tracks/13158665/download",
#  "playback_count": 0,
#  "download_count": 0,
#  "favoritings_count": 0,
#  "comment_count": 0,
#  "created_with": {
#    "id": 124,
#    "name": "SoundCloud iPhone",
#    "uri": "http://api.soundcloud.com/apps/124",
#    "permalink_url": "http://soundcloud.com/apps/iphone"
#  },
#  "attachments_uri": "http://api.soundcloud.com/tracks/13158665/attachments"
#}
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
#asset_data     binary data of the audio file     (only for uploading)
#artwork_data     binary data of the artwork image     (only for uploading)
#user_favorite     track favorite of current user (boolean, authenticated requests only)     1
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()
        print('Data saved in '+dbFileName)

def main(): 
    getNewSnowballSample(15)
    printData() 
