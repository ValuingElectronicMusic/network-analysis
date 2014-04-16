'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud  # @UnresolvedImport
import process_scdb_data as pscd

import clientSettings as client
client = soundcloud.Client(client_id=client.get_client_id())

import sqlite3
import time

requestCount = 0

try:
    import cPickle as pickle
except:
    import pickle

# The following global variables represent information about the SoundCloud users in our
# sample set. We only collect data on users in our sample set, discarding other data
# For each set of SoundCloud *objects* (excluding sets of tuples), 
# we maintain a list of ids of members in that set.
# This is to avoid duplicates appearing in the set, due to two identical SoundCloud
# objects not being recognised as being the same object.
  
# users = set of SoundCloud user objects
users = set()
user_ids_collected = set()
user_ids_to_collect = set()
# x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "users")
x_follows_y = set()
# tracks = set of SoundCloud track objects where tracks belong to users in "users"
# NB tracks does *not* include tracks by non-sampled users, even if a sampled user has commented or favourited that track
# ids of these tracks can be obtained through the relevant fields in the favourites/comments sets
# and the ids can be used to get more information from SoundCloud on those tracks if required  
tracks = set()
track_ids_collected = set()
# TODO add the four items below as DB tables
# groups - set of tuples representing SoundCloud groups that a user has joined
groups = set()
# favourites (NB English spelling here, US spelling on SoundCloud) 
#    - set of tuples representing tracks that a user has 'liked'
favourites = set()
# comments - set of SoundCloud comments for a particular track
comments = set()
comment_ids_collected = set()
# playlists - set of SoundCloud users' playlisted tracks
playlists = set()


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
            
    global groups
    print ''
    print('groups (max 10 selected at random from '+str(len(groups))+' groups)')
    temp_copy = groups.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped[0])+' is in group id: '+str(popped[1]))
        count = count+1

    global favourites
    print ''
    print('User-favourited tracks (max 10 selected at random from '+str(len(favourites))+' user-favourite-track relationships)')
    temp_copy = favourites.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1

    global comments
    print ''
    print('User comments (max 10 selected at random from '+str(len(comments))+' comments from all users)')
    temp_copy = comments.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. user id: '+str(popped.user_id)+' on track '+str(popped.track_id)+': '+popped.body)
        count = count+1

def getUserId(username):
    try:
        print('resolve user '+username)
        userId = client.get('/resolve', url='https://soundcloud.com/'+username)
        return userId.id
    except Exception:
        print('invalid username given')
        return None
    
def getUser(username):
    ''' Returns a SoundCloud object with the data for the username given in the parameter'''
     
    try:
        print('resolve user '+username)
        user = client.get('/resolve', url='https://soundcloud.com/'+username)
        return user
    except Exception:
        print('invalid username given')
        return None
        
def getRandomUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            userfound = True    
    return user

def getRandomLondonEMUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            city = lowerCaseStr(user.city)
            country = lowerCaseStr(user.country)
            print('Trying user '+str(userId)+' city '+city)
            if ('london' in city):               
                print('            '+str(userId)+' city '+city+' country '+country+' with '+str(user.track_count)+' tracks')
                if (('britain' in country) or ('united kingdom' in country)): 
                    user_tracks = client.get('/users/'+str(userId)+'/tracks')
                    for track in user_tracks:
                        tag_list = lowerCaseStr(track.tag_list)
                        genre = lowerCaseStr(track.genre)
                        print('************'+str(track.id)+' genre '+genre+' tag_list '+tag_list)
                        if (('electronic' in tag_list) or ('electronic' in genre)):
                            userfound = True
                            break 
    print('London-based Electronic music User found: '+str(userId))
    return user

def getRandomLondonUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            city = lowerCaseStr(user.city)
            country = lowerCaseStr(user.country)
            print('Trying user '+str(userId)+' city '+city)
            if ('london' in city):               
                print('            '+str(userId)+' city '+city+' country '+country)
                if (('britain' in country) or ('united kingdom' in country)): 
                    userfound = True
                    break 
    print('London-based User found: '+str(userId))
    return user

def getRandomEMUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            print('Trying user '+str(userId)+' with '+str(user.track_count)+' tracks')
            user_tracks = client.get('/users/'+str(userId)+'/tracks')
            for track in user_tracks:
                tag_list = lowerCaseStr(track.tag_list)
                genre = lowerCaseStr(track.genre)
                print('*******************************************'+str(track.id)+' genre '+genre+' tag_list '+tag_list)
                if (('electronic' in tag_list) or ('electronic' in genre)):
                    userfound = True
                    break 
    print('Electronic music User found: '+str(userId))
    return user


def lowerCaseStr(inputText):
    return str.lower(unicode(inputText).encode('utf-8'))

def getXUserIDs(limit=10):
    temp_users = set()
    for i in range(0,limit):  # @UnusedVariable
        #print i
        temp_users.add(getRandomUser().id)
    return temp_users


def getAllFollowers(user):
    global users
    strUserID = str(user.id)
    followers = clientGet('/users/'+strUserID+'/followers')
    print(str(len(users))+' users collected. Exploring followers of User '+ strUserID+' with '+str(len(followers))+' followers')
    return followers


def getAllFollowings(user):
    global users
    strUserID = str(user.id)
    followings = clientGet('/users/'+strUserID+'/followings')
    print(str(len(users))+' users collected. Exploring following activities of User '+ strUserID+' who follows '+str(len(followings))+' users')
    return followings


def clientGet(request, maxAttempts=100):
    global requestCount
    success = False;
    count = 0
    result = None
    timeDelay = 2 # time delay in seconds between failed attempts
    
    while(not(success) and (count<maxAttempts)):
        try:
            result = client.get(request)
            success = True
            break
        except Exception as e:
            count = count+1
            time.sleep(timeDelay)
            print('Problem connecting to SoundCloud client, error '+str(e)+'. Trying again... attempt '+str(count)+' of '+str(maxAttempts))
    if (not(success)):
        print('***Unable to retrieve information from SoundCloud for the request: '+request)
    requestCount = requestCount+count+1
    if (requestCount>=25):   # every 25 times we request data from SoundCloud, pause (to avoid overloading the server)
        time.sleep((5*timeDelay))
        requestCount = 0
    return result
            
            

def getNewSnowballSample(sample_size=500,desired_seed_users=set()):
    '''Generates a new sample of users (set to the specified sample size, default 500), also generating 
     data on those users' tracks and how the users interact with other users on SoundCloud.
     N.B. This builds on any previously collected samples that are stored in scdb.sqlite   
     To call this function, give the parameters as an integer (number of users needed) and 
     a set of userIds that you would like the function to use as starting points, 
     e.g. getNewSnowballSample(1000, {83918, 1479884, 5783})       

    ALGORITHM
    DONE get desired_samplesize and ids of desired seed users
    DONE read in data collected so far
    read in cpickle of sets of ids collected/to-collect
    DONE add ids of desired seed users to user_ids_to_collect
    DONE repeat until size(user_ids_collected) == desired_samplesize:    
        DONE print 'x/n total users collected so far. Collecting the next batch of 100 users'
        DONE call batchDataCollection function
        DONE print 'Pausing for 10 seconds' 
        NB this is the time window when we can interrupt batchDataCollection 
        NB I've chosen 10 seconds sleep, slightly arbitrarily, based on experiments so far
    done'''
    global users
    global tracks
    global x_follows_y
    global favourites
    global comments
    global groups
    global playlists
    global user_ids_collected
    global user_ids_to_collect
    global track_ids_collected
    global comment_ids_collected
    
    # read in data collected so far
    data = pscd.data_holder()

    users = data.users
    tracks = data.tracks
    x_follows_y = data.x_follows_y
    favourites = data.favourites
    comments = data.comments
    groups = data.groups
    playlists = data.playlists
    
    # read in cpickle of sets of ids collected/to-collect
    # set default of empty sets for each set of ids, to be replaced by the cpickle contents
    user_ids_to_collect = set()
    user_ids_collected = set()
    track_ids_collected = set()
    comment_ids_collected = set()
    try:
        current_ids = pickle.load(open("current_ids.p", "rb"))
        user_ids_to_collect = current_ids['u_ids_to_collect']
        user_ids_collected = current_ids['u_ids_collected']
        track_ids_collected = current_ids['t_ids_collected']
        comment_ids_collected = current_ids['c_ids_collected']
    except: 
        pass # use default values of empty sets for any id sets not initialised

    # add ids of desired seed users to user_ids_to_collect
    user_ids_to_collect = user_ids_to_collect.union(desired_seed_users)
    print('Generating snowball sample with a sample size of '+str(sample_size))
    #repeat until size(user_ids_collected) == desired_samplesize:
    
    while (len(user_ids_collected)<sample_size):
        print(str(len(user_ids_collected))+'/'+str(sample_size)+' total users collected so far. Collecting the next batch of 100 users')
        batchDataCollection()
	print 'Pausing for 10 seconds - if you want to interrupt data collection, do it now.'
	# this is the time window when we can interrupt batchDataCollection 
	# NB I've chosen 10 seconds sleep, slightly arbitrarily, based on experiments so far
        time.sleep(10) # wait 10 seconds to give the server a break
        print 'Finished pausing, time for more data collection - now please wait till the next pause if you want to interrupt data collection'
############################ OLD ######################
#         if (len(user_ids_to_collect) ==0):
#             user = getRandomUser() # get a new starting point at random        
#         else:
#             userId = user_ids_to_collect.pop(0)
#             user = clientGet('/users/'+str(userId)) 
# #         print('User id currently = '+str(user.id))
#         if (not(user.id in user_ids_collected)): # Have we already added this u
#             users.add(user)
#             user_ids_collected.append(user.id)
#             print('Seed user = '+str(user.id))
#             if (len(users)<sample_size):  #in case adding the new user to our sample brings us to our desired samplesize
#                 collectFollowLinksFromSeedUser(user,sample_size)
#         
#     # populate the contents of the remaining global variables  with data relating to the new sample of users
#     getTracks()
#     getFavourites()
#     getGroups()
#     getPlaylists()
#     getComments()

     
# def getNewSnowballSample(sample_size=10):
#     ''' Generates a new sample of users (set to the specified sample size, default 10), also generating 
#     data on those users' tracks and follow relationships between the users in the set 
#     N.B. This wipes any previously collected samples that are only stored in local memory '''    
#     global users
#     global user_ids_collected
#     global user_ids_to_collect
#     global tracks
#     global track_ids_collected
#     global x_follows_y
#     global groups
#     global favourites
#     global comments
#     global comment_ids_collected
#     users = set() # initialised to empty
#     user_ids_collected = list()
#     user_ids_to_collect = list()
#     x_follows_y = set() # initialised to empty
#     tracks = set() # initialised to empty
#     track_ids_collected = list()
#     groups = set() # initialised to empty
#     favourites = set() # initialised to empty
#     comments = set() # initialised to empty
#     comment_ids_collected = list()
#     print('Generating snowball sample with a sample size of '+str(sample_size))
#     while (len(users)<sample_size):
# #         print(str(sample_size)+' sample_size '+ str(len(users))+' users '+', explore: '+str(user_ids_to_collect)+' added: '+str(user_ids_collected))
#         if (len(user_ids_to_collect) ==0):
#             user = getRandomUser() # get a new starting point at random        
#         else:
#             userId = user_ids_to_collect.pop(0)
#             user = clientGet('/users/'+str(userId)) 
# #         print('User id currently = '+str(user.id))
#         if (not(user.id in user_ids_collected)): # Have we already added this u
#             users.add(user)
#             user_ids_collected.append(user.id)
#             print('Seed user = '+str(user.id))
#             if (len(users)<sample_size):  #in case adding the new user to our sample brings us to our desired samplesize
#                 collectFollowLinksFromSeedUser(user,sample_size)
#         
#     # populate the contents of the remaining global variables  with data relating to the new sample of users
#     getTracks()
#     getFavourites()
#     getGroups()
#     #getPlaylists()
#     getComments()


def batchDataCollection(batch_size=100):
    ''' Batch function to collect x number of users (default 100) and all assorted data
	read in cpickle and DB information from previous runs into runtime memory
	num_users_collected = 0
	repeat until 100 users collected:
		if the user_ids_to_collect set is nonempty:      
			pop a user_id from the set and set that user_id as seed.
		else: set random user as seed
		
		# below, 'collect'='get data from soundcloud API, store in relevant internal data structure'
		# if an item has already been collected, collect it again and check if 
		# the collected info needs updating 
		# (we want to have the most up to date information)
	        call collectFollowsAndFollowersData(user)
	        call collectFavouritedTracksData(user)
	        call collectGroupsData(user)
	        call collectProducedTracksData(user)
	        call collectCommentsData(user)
	        call collectPlaylistData(user)
		# now finished with this user, move onto the next user until 100 users collected
		num_users_collected++
	# (go back to the start of the repeat loop again)
	
	# Now we have collected 100 users
	call backupData 
	# done
	'''
    global users
    global tracks
    global x_follows_y
    global favourites
    global comments
    global groups
    global playlists
    global user_ids_collected
    global user_ids_to_collect
    global track_ids_collected
    global comment_ids_collected
    print 'TODO BatchCollection'

def collectFollowsAndFollowersData(user):
    '''collect ids of all users that our seed user follows: 
 		construct follows relationship tuple for each follow (seed_id, followed_user_id)
		add ids to user_ids_to_collect
       then collect ids of all users that follow our seed user:
		construct follows relationship tuple for each follow (follower_user_id, seed_id)
		add ids to user_ids_to_collect
    '''
    print 'TODO CollectFollowsAndFollowersData'

def collectFavouritedTracksData(user):
    ''' collect all the user's favourited tracks
		construct favourites tuple for each favouriting: (user_id, track_id, track_producer_id)
		collect track information and add track_id to track_ids_collected
		add all track_producer_ids to user_ids_to_collect
    '''
    print 'TODO CollectFavouritedTracksData'
	
def collectGroupsData(user): 
    ''' collect all the user's groups
		construct tuple (seed_id, group_id, group_name)
    '''
######################## NB a group is created by a user. 
######################## Is joining a group a measure of influence of the *creator* of the group?
######################## If so, add group_creator_id to tuple and to user_ids_to_collect
    print 'TODO CollectGroupsData'

def collectProducedTracksData(user):
    ''' collect all tracks produced by seed user
	 for each track:
		collect all comments made on seed user's tracks
		for each comment collected on seed user's track:
			add comment id to comment_ids_collected
			collect user id and add to user_ids_to_be_collected
    '''
    print 'TODO CollectProducedTracksData'

def collectCommentsData(user):
    ''' collect all comments made by seed user
    for each comment:
		add comment id to comment_ids_collected
		collect track information and add track id to track_ids_collected
		add track_creator_id to user_ids_to_collect
    '''
    print 'TODO CollectCommentsData'

def collectPlaylistData(user):
    '''	collect all playlists by the user
		construct playlist tuple for each playlisted track: (user_id, playlist_id,track_id, track_producer_id)
		collect track information and add track_id to track_ids_collected
		add all track_producer_ids to user_ids_to_collect 
    ''' 
    print 'TODO CollectPlaylistsData'


def backupData():
    '''
        { backup: (grandfather - father - son: grandfather is the oldest backup,
        # father is the most recent backup, son is the current version)
        check time:
                if current_time>=24 hours later than last_backup_timestamp:
                last_backup_timestamp = current_time
                copy grandfatherDB+pickle to backup files called '<current_time>-BK-scdb.sqlite' and <current-time>-BK-whate$
                else: pass # (do nothing, leave last_backup_timestamp with the value it currently has)
        # do this every time, regardless of current_time
        copy fatherDB+pickle to grandfatherDB+pickle
        copy sonDB+pickle to fatherDB+pickle
        save current information to sonDB+pickle # save updated DB tables and cpickle
    
    '''
    global user_ids_to_collect
    global user_ids_collected
    global track_ids_collected
    global comment_ids_collected
    current_ids = dict()
    current_ids['u_ids_to_collect'] = user_ids_to_collect
    current_ids['u_ids_collected'] = user_ids_collected
    current_ids['t_ids_collected'] = track_ids_collected
    current_ids['c_ids_collected'] = comment_ids_collected
    
    #do grandfather father son backup
    
    pickle.dump(current_ids, open("current_ids.p", "wb"))
    

########################OLD 
def collectFollowLinksFromSeedUser(user,sampleSize):
    ''' Populate the users and x_follows_y sets with data sampled from SoundCloud '''
    global users
    global user_ids_collected
    global x_follows_y
    global user_ids_to_collect
    # look for all followers of user    
    followers = getAllFollowers(user)
    # process each follower
    for follower in followers:
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((follower.id, user.id))
        # Add the follower to the list of SC users to be explored (if not already added) 
        if (not(follower.id in user_ids_collected)):
            user_ids_to_collect.append(follower.id)
      
    # look for all followings of user (i.e. all users that our seed user follows)    
    followings = getAllFollowings(user)

    # process each user that the seed user follows (= followings)
    for following in followings:
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((user.id, following.id))
        # Add the follower to the list of SC users to be explored (if not already added) 
        if (not(following.id in user_ids_collected)):
            user_ids_to_collect.append(following.id)


def getTracks():
    print 'Getting data about tracks produced by sampled users...'
    global users
    global tracks
    global track_ids_collected
    for user in users:
        u_id = user.id 
        user_tracks = clientGet('/users/'+str(u_id)+'/tracks')
        for u_track in user_tracks:
            if (not(u_track.id in track_ids_collected)):
                tracks.add(u_track)
                track_ids_collected.append(u_track.id)
    
    
def getGroups():
    print 'Getting data about sampled users\' groups...'
    global users
    global groups
    for user in users:
        u_id = user.id 
        user_groups = clientGet('/users/'+str(u_id)+'/groups')
        for u_group in user_groups:
            if (not(u_group in groups)):
                groups.add((u_id, u_group.id))

        
def getFavourites():
    print 'Getting data about sampled users\' favourited tracks...'
    global users
    global favourites
    for user in users:
        u_id = user.id 
        user_favourites = clientGet('/users/'+str(u_id)+'/favorites') # Note US spelling
        for u_favourite in user_favourites:
            favourites.add((u_id, u_favourite.id))    
    
    
def getComments():
    print 'Getting data about all comments made by sampled users...'
    global users
    global comments
    global comment_ids_collected
    for user in users:
        u_id = user.id 
        user_comments = clientGet('/users/'+str(u_id)+'/comments')
        for u_comment in user_comments:
            if (not(u_comment.id in comment_ids_collected)):
                comments.add(u_comment)
                comment_ids_collected.append(u_comment.id)
    
 
def getPlaylists():
    print 'Getting data about users\' playlists... '
    global users
    global playlists
    for user in users:
        u_id = user.id 
        user_playlists = clientGet('/users/'+str(u_id)+'/playlists') 
        for u_playlist in user_playlists:
            for u_track in u_playlist.tracks:
                playlists.add((u_id, u_playlist.id, u_track.id))



def exportDataToSQLite():
    global users
    global x_follows_y
    global tracks
    print '' # for neater display 
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
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, 
                             permalink_url TEXT, full_name TEXT, description TEXT,  
                             city TEXT, country TEXT, 
                             track_count INTEGER, playlist_count INTEGER, 
                             followers_count INTEGER, followings_count INTEGER, public_favorites_count INTEGER)''')
        print('Adding data to users table in DB.... Total num of users: '+str(len(users)))
        for user in users:
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
        #issue with label_id? label_id field removed (can use 'label_name' to detect existence of a label)
        # issue with playback_count? playback_count removed 
        print 'Creating tracks table in DB....'
        cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(
        id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT,   
        permalink_url TEXT,  track_type TEXT, state TEXT, created_at TEXT, 
        original_format TEXT, description TEXT, sharing TEXT,   
        genre TEXT, duration INTEGER, key_signature TEXT, bpm INTEGER, 
        license TEXT, label_name TEXT, 
        favoritings_count INTEGER, 
        streamable TEXT, stream_url TEXT, 
        downloadable TEXT, download_count INTEGER, 
        commentable TEXT,
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
        license, label_name,
        favoritings_count, 
        streamable, stream_url, 
        downloadable, download_count, 
        commentable, 
        purchase_url, artwork_url, video_url, embeddable_by,
        release, release_month, release_day, release_year,  
        tag_list)  
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                   ?)''',
                (track.id, track.user_id, track.title,   
                track.permalink_url, track.track_type, track.state, track.created_at, 
                track.original_format, track.description, track.sharing,   
                track.genre, track.duration, track.key_signature, track.bpm, 
                track.license, track.label_name,
                track.favoritings_count, 
                track.streamable, track.stream_url, 
                track.downloadable, track.download_count, 
                track.commentable, 
                track.purchase_url, track.artwork_url, track.video_url, track.embeddable_by,
                track.release, track.release_month, track.release_day, track.release_year,  
                track.tag_list)) 
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
        # TODO  - but leave this for now
        
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
