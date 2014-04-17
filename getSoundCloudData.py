'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud  # @UnresolvedImport
#import process_scdb_data as pscd

import clientSettings
import time
import sqlite3

try:   # not all Python implementations have cPickle, pickle is a slower alternative
    import cPickle as pickle
except:
    import pickle
db_path = 'scdb.sqlite'
client = soundcloud.Client(client_id=clientSettings.get_client_id())
request_count = 0
time_delay = 2 # time delay in seconds between failed attempts

def get_table(table_name):
    '''Returns a set of the contents of one entire table from the sqlite database.'''
    global db_path
    try:
        conn = sqlite3.connect(db_path)
        with conn:
            curs = conn.cursor()
            curs.execute("SELECT * FROM {!s}".format(table_name))
            return set(curs.fetchall())  # list returned by curs.fetchall(), transformed to set
    except Exception:
        # for some reason, table contents couldn't be retrieved
        # Just return an empty set in place of a set of contents
        return set()
    
def get_pickled_data(pickled_data, ids_set_wanted):
    ''' Returns a set of data from within the pickled data on ids to collect/collected. 
        Handles exceptions, returning a blank set if the desired data is not in the pickled data'''
    try:
        return pickled_data[ids_set_wanted]   # this is a set
    except:
        return set()
    

class SC_data():
    
    def __init__(self):
        # The following class variables represent data about the SoundCloud users in our
        # sample set. We collect all data relating to users in our sample set
        print '1. reading DATA from DB'  
        # DATA OBTAINED FROM SOUNDCLOUD API
        # users = set of SoundCloud user objects
        self.users = get_table('users')
        # tracks = set of SoundCloud track objects which users in "users" have interacted with
        self.tracks = get_table('tracks')
        # x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "users")
        self.x_follows_y = get_table('x_follows_y')
        # TODO add the four items below as DB tables
        # favourites (NB UK spelling here, US spelling on SoundCloud) 
        #    - set of tuples representing tracks that a user has 'liked'
        self.favourites = get_table('favourites')
        # groups - set of tuples representing SoundCloud groups that a user has joined
        self.groups = get_table('groups')
        # comments - set of SoundCloud comments for a particular track
        self.comments = get_table('comments')
        # playlists - set of SoundCloud users' playlisted tracks
        self.playlists = get_table('playlists')
       
        print '2. unpickling FURTHER DATA'
        # FURTHER DATA 
        # For various SoundCloud data (especially SoundCloud objects), 
        # we maintain a list of ids of members in that set.
        # This is to assist data collection and also to avoid duplicates appearing
        # in the set, due to two identical SoundCloud
        # objects not being recognised as being the same object.
        
        # read in cpickle of sets of ids collected/to-collect
        try:
            current_ids = pickle.load(open("current_ids.p", "rb")) # this may throw an exception
        except:            
            # set default of empty sets for each set of ids if there is no cPickle data
            print 'No data available on previous batches collected/users to collect data on. Initialising...'
            self.user_ids_to_collect = set()
            self.user_ids_collected = set()
            self.track_ids_collected = set()
            self.comment_ids_collected = set()
        else:
            self.user_ids_to_collect = get_pickled_data(current_ids, 'u_ids_to_collect')
            self.user_ids_collected = get_pickled_data(current_ids, 'u_ids_collected')
            self.track_ids_collected = get_pickled_data(current_ids, 't_ids_collected')
            self.comment_ids_collected = get_pickled_data(current_ids, 'c_ids_collected')
        
    def print_data_summary(self):
        print(str(len(self.users))+' users, '+ 
              str(len(self.tracks))+' tracks, '+
              str(len(self.x_follows_y))+' follows, '+
              str(len(self.favourites))+' favourites, '+
              str(len(self.groups))+' groups, '+
              str(len(self.users))+' comments, '+
              str(len(self.playlists))+' playlists.')

def peek_at_collection(collection_being_peeked, max=5):
    if (len(collection_being_peeked)==0):
        print('This data collection is empty')
    else: 
        print('Here is a list of (max) '+str(max)+' members of the collection (with '+str(len(collection_being_peeked))+' members):')
        count=0;
        for n in collection_being_peeked:
            count = count+1
            print(str(count)+': '+str(n))
            if (count>=max):
                break

    
def get_user_id_from_username(username):
    try:
        print('resolve user '+username)
        userId = client.get('/resolve', url='https://soundcloud.com/'+username)
        return userId.id
    except Exception:
        print('invalid username given')
        return None
    
def get_user_from_username(username):
    ''' Returns a SoundCloud object with the data for the username given in the parameter'''
     
    try:
        print('resolve user '+username)
        user = client.get('/resolve', url='https://soundcloud.com/'+username)
        return user
    except Exception:
        print('invalid username given')
        return None
        
def get_random_user():
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

def get_random_london_EM_user():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            city = lower_case_str(user.city)
            country = lower_case_str(user.country)
            print('Trying user '+str(userId)+' city '+city)
            if ('london' in city):               
                print('            '+str(userId)+' city '+city+' country '+country+' with '+str(user.track_count)+' tracks')
                if (('britain' in country) or ('united kingdom' in country)): 
                    user_tracks = client.get('/users/'+str(userId)+'/tracks')
                    for track in user_tracks:
                        tag_list = lower_case_str(track.tag_list)
                        genre = lower_case_str(track.genre)
                        print('************'+str(track.id)+' genre '+genre+' tag_list '+tag_list)
                        if (('electronic' in tag_list) or ('electronic' in genre)):
                            userfound = True
                            break 
    print('London-based Electronic music User found: '+str(userId))
    return user

def get_random_london_user():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception:
            pass
        else:
            city = lower_case_str(user.city)
            country = lower_case_str(user.country)
            print('Trying user '+str(userId)+' city '+city)
            if ('london' in city):               
                print('            '+str(userId)+' city '+city+' country '+country)
                if (('britain' in country) or ('united kingdom' in country)): 
                    userfound = True
                    break 
    print('London-based User found: '+str(userId))
    return user

def get_random_EM_user():
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
                tag_list = lower_case_str(track.tag_list)
                genre = lower_case_str(track.genre)
                print('*******************************************'+str(track.id)+' genre '+genre+' tag_list '+tag_list)
                if (('electronic' in tag_list) or ('electronic' in genre)):
                    userfound = True
                    break 
    print('Electronic music User found: '+str(userId))
    return user

#def getXUserIDs(limit=10):
#    temp_users = set()
#    for i in range(0,limit):  # @UnusedVariable
#        #print i
#        temp_users.add(get_random_user().id)
#    return temp_user 


def get_all_followers(user_id):
    return client_get('/users/'+str(user_id)+'/followers')
    
def get_all_followings(user_id):
    return client_get('/users/'+str(user_id)+'/followings')

def client_get(request, max_attempts=100):
    global client
    global request_count
    global time_delay
    success = False;
    count = 0
    result = None
    
    while(not(success) and (count<max_attempts)):
        try:
            result = client.get(request)
            success = True
            break
        except Exception as e:
            count = count+1
            time.sleep(time_delay)
            print('Problem connecting to SoundCloud client, error '+str(e)+'. Trying again... attempt '+str(count)+' of '+str(max_attempts))
    if (not(success)):
        print('***Unable to retrieve information from SoundCloud for the request: '+request)
    request_count = request_count+count+1
    if (request_count>=25):   # every 25 times we request data from SoundCloud, pause (to avoid overloading the server)
        time.sleep((5*time_delay))
        request_count = 0
    return result

def lower_case_str(inputText):
    return str.lower(unicode(inputText).encode('utf-8'))

            

def get_new_snowball_sample(sample_size=500, desired_seed_users=set(), batch_size=100, pause_between_batches=10):
    '''Generates a new sample of users (set to the specified sample size, default 500), also generating 
     data on those users' tracks and how the users interact with other users on SoundCloud.
     N.B. This builds on any previously collected samples that are stored in scdb.sqlite   
     To call this function, give the parameters as an integer (number of users needed) and 
     a set of userIds that you would like the function to use as starting points, 
     e.g. get_new_snowball_sample(1000, {83918, 1479884, 5783})       

    ALGORITHM
    DONE get desired_samplesize and ids of desired seed users
    DONE read in data collected so far and cpickle of sets of ids collected/to-collect
    DONE add ids of desired seed users to user_ids_to_collect
    DONE repeat until size(user_ids_collected) == desired_samplesize:    
        DONE print 'x/n total users collected so far. Collecting the next batch of 100 users'
        DONE call batch_data_collection function
        DONE print 'Pausing for x seconds' 
        NB this is the time window when we can interrupt batch_data_collection 
        NB I've chosen 10 seconds sleep, slightly arbitrarily, based on experiments so far
    done'''
    
    # read in data collected so far
    data = SC_data()

    # add ids of desired seed users to user_ids_to_collect
    data.user_ids_to_collect = data.user_ids_to_collect.union(desired_seed_users)
    print('Generating snowball sample with a sample size of '+str(sample_size))
    #repeat until size(user_ids_collected) == desired_samplesize:
    while (len(data.user_ids_collected)<sample_size):
        # NB Python passes parameters by reference so any changes made by the called method will propagate through to the caller
        num_still_to_collect = sample_size - len(data.user_ids_collected)
        if (num_still_to_collect>=batch_size):
            print(str(len(data.user_ids_collected))+'/'+str(sample_size)+' total users collected so far. Collecting the next batch of '+str(batch_size)+' users')
            batch_data_collection(data, batch_size)
        else: 
            print(str(len(data.user_ids_collected))+'/'+str(sample_size)+' total users collected so far. Collecting the next batch of '+str(num_still_to_collect)+' users')
            batch_data_collection(data, num_still_to_collect)  
	print('Pausing for '+str(pause_between_batches)+' seconds. You can interrupt data collection now by pressing Ctrl-C')
	# this is the time window when we can interrupt batch_data_collection 
	# NB I've chosen 10 seconds sleep, slightly arbitrarily, based on experiments so far
        time.sleep(pause_between_batches) # wait 10 seconds to give the server a break
        print 'Finished pausing, time for more data collection - please do not interrupt...'
    print('Snowball sample fully collected with a sample size of '+str(len(data.user_ids_collected))+' users.')
     
# def get_new_snowball_sample(sample_size=10):
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
#             user = get_random_user() # get a new starting point at random        
#         else:
#             userId = user_ids_to_collect.pop(0)
#             user = client_get('/users/'+str(userId)) 
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


def batch_data_collection(data, batch_size):
    ''' Batch function to collect x number of users and all assorted data
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
	call backupData and save collected data externally
	# done
	'''
    # repeat until 100 users collected:
    num_users_to_be_collected = len(data.user_ids_collected)+batch_size
    while(len(data.user_ids_collected) < num_users_to_be_collected):
        if (len(data.user_ids_to_collect)==0):
            seed_user = get_random_user()
        else: 
            seed_user = client_get('/users/'+str(data.user_ids_to_collect.pop()))
        data.user_ids_collected.add(seed_user.id)
        peek_at_collection(data.user_ids_collected)
#        if the user_ids_to_collect set is nonempty:      
#            pop a user_id from the set and set that user_id as seed.
#        else: set random user as seed
#        
#        # below, 'collect'='get data from soundcloud API, store in relevant internal data structure'
#        # if an item has already been collected, collect it again and check if 
#        # the collected info needs updating 
#        # (we want to have the most up to date information)
#            call collectFollowsAndFollowersData(user)
#            call collectFavouritedTracksData(user)
#            call collectGroupsData(user)
#            call collectProducedTracksData(user)
#            call collectCommentsData(user)
#            call collectPlaylistData(user)
#        # now finished with this user, move onto the next user until 100 users collected
#        num_users_collected++
#    # (go back to the start of the repeat loop again)
#    
#    # Now we have collected 100 users
#    call backupData 
#    # done
    
    ############################ OLD ######################
#         if (len(user_ids_to_collect) ==0):
#             user = get_random_user() # get a new starting point at random        
#         else:
#             userId = user_ids_to_collect.pop(0)
#             user = client_get('/users/'+str(userId)) 
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
    global db_path
    
    #do grandfather father son backup
    
    pickle.dump(current_ids, open("current_ids.p", "wb"))
    print('Latest snapshot of data stored in '+db_path+' database.')


########################OLD 
def collectFollowLinksFromSeedUser(user,sampleSize):
    ''' Populate the users and x_follows_y sets with data sampled from SoundCloud '''
    global users
    global user_ids_collected
    global x_follows_y
    global user_ids_to_collect
    # look for all followers of user    
    followers = get_all_followers(user.id)
    # process each follower
    for follower in followers:
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((follower.id, user.id))
        # Add the follower to the list of SC users to be explored (if not already added) 
        if (not(follower.id in user_ids_collected)):
            user_ids_to_collect.append(follower.id)
      
    # look for all followings of user (i.e. all users that our seed user follows)    
    followings = get_all_followings(user.id)

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
        user_tracks = client_get('/users/'+str(u_id)+'/tracks')
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
        user_groups = client_get('/users/'+str(u_id)+'/groups')
        for u_group in user_groups:
            if (not(u_group in groups)):
                groups.add((u_id, u_group.id))

        
def getFavourites():
    print 'Getting data about sampled users\' favourited tracks...'
    global users
    global favourites
    for user in users:
        u_id = user.id 
        user_favourites = client_get('/users/'+str(u_id)+'/favorites') # Note US spelling
        for u_favourite in user_favourites:
            favourites.add((u_id, u_favourite.id))    
    
    
def getComments():
    print 'Getting data about all comments made by sampled users...'
    global users
    global comments
    global comment_ids_collected
    for user in users:
        u_id = user.id 
        user_comments = client_get('/users/'+str(u_id)+'/comments')
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
        user_playlists = client_get('/users/'+str(u_id)+'/playlists') 
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
    get_new_snowball_sample(sampleSize)
    #printData() 
    exportDataToSQLite()
