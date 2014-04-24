'''
Created on Feb 25, 2014

@author: annajordanous
'''

# TODO log errors plus calls to client get in external log files 

import random
import soundcloud  
#import process_scdb_data as pscd

import client_settings
import time
import sqlite3
import logging
import logging
logging.basicConfig(filename='logs/log'+time.strftime('%Y%m%d-%H%M')+'.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

import add_data as ad 

try:   # not all Python implementations have cPickle, pickle is a slower alternative
    import cPickle as pickle
except:
    import pickle
db_path = 'scdb.sqlite'
client = soundcloud.Client(client_id=client_settings.get_client_id())
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
        # favourites (NB UK spelling here, US spelling on SoundCloud) 
        #    - set of tuples representing tracks that a user has 'liked'
        self.favourites = get_table('favourites')
        # groups - set of tuples representing data on SoundCloud groups involving sampled users 
        self.groups = get_table('groups')
        # group_membership - set of tuples representing SoundCloud groups a user is member of
        self.group_mem = get_table('group_mem')
        # comments - set of SoundCloud comments for a particular track
        self.comments = get_table('comments')
        # playlists - set of SoundCloud users' playlisted tracks
        self.playlists = get_table('playlists')
        
        # The following table creators are for the _deriv database.
        self.genres = get_table('genres')
        self.tags = get_table('tags')
        self.user_genres = get_table('user_genres')
        self.user_tags = get_table('user_tags')
        self.x_faves_work_of_y = get_table('x_faves_work_of_y')
        self.comments_corp = get_table('comments_corp')
   
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
            self.group_ids_collected = set()
        else:
            self.user_ids_to_collect = get_pickled_data(current_ids, 'u_ids_to_collect')
            self.user_ids_collected = get_pickled_data(current_ids, 'u_ids_collected')
            self.track_ids_collected = get_pickled_data(current_ids, 't_ids_collected')
            self.comment_ids_collected = get_pickled_data(current_ids, 'c_ids_collected')
            self.group_ids_collected = get_pickled_data(current_ids, 'g_ids_collected')
            
    def print_data_summary(self):
        print(str(len(self.users))+' users, '+ 
              str(len(self.tracks))+' tracks, '+
              str(len(self.x_follows_y))+' follows, '+
              str(len(self.favourites))+' favourites, '+
              str(len(self.groups))+' groups, '+
              str(len(self.group_mem))+' group memberships, '+
              str(len(self.users))+' comments, '+
              str(len(self.playlists))+' playlisted tracks.')
        print('Derived data: '+
              str(len(self.genres))+' genres'+
              str(len(self.tags))+' tags'+
              str(len(self.user_genres))+' user genres'+
              str(len(self.user_tags))+' user tags'+
              str(len(self.x_faves_work_of_y))+' x_faves_work_of_y'+ 
              str(len(self.comments_corp))+' in comments corpus')


def peek_at_collection(collection_being_peeked, maximum=5):
    if (len(collection_being_peeked)==0):
        print('This data collection is empty')
    else: 
        print('Here is a list of (maximum) '+str(maximum)+' members of the collection (with '+str(len(collection_being_peeked))+' members):')
        count=0;
        for n in collection_being_peeked:
            count = count+1
            print(str(count)+': '+str(n))
            if (count>=maximum):
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
            print('Problem connecting to SoundCloud client, error '+str(e)+' for request '+request+'. Trying again... attempt '+str(count)+' of '+str(max_attempts))
    if (not(success)):
        print('***Unable to retrieve information from SoundCloud for the request: '+request)
    request_count = request_count+count+1
    if (request_count>=25):   # every 25 times we request data from SoundCloud, pause (to avoid overloading the server)
        #print('pausing after '+str(request_count)+' requests made') # TODO remove
        time.sleep(time_delay)
        request_count = 0
        #print('finished pausing') # TODO remove
    return result

def lower_case_str(inputText):
    return str.lower(unicode(inputText).encode('utf-8'))

            

def get_new_snowball_sample(sample_size=500, desired_seed_users=set(), batch_size=100, pause_between_batches=10):
    '''Generates a new sample of users (set to the specified sample size, default 500), also generating 
     data on those users' tracks and how the users interact with other users on SoundCloud.
     N.B. This builds on any previously collected samples that are stored in scdb.sqlite   
     To call this function, give the parameters as an integer (number of users needed) and 
     a set of userIds that you would like the function to use as starting points, 
     e.g. gsc.get_new_snowball_sample(sample_size=10, desired_seed_users={63287951}, 
     batch_size=2, pause_between_batches=2)     

    ALGORITHM
    get desired_samplesize and ids of desired seed users
    read in data collected so far and cpickle of sets of ids collected/to-collect
    add ids of desired seed users to user_ids_to_collect
    repeat until size(user_ids_collected) == desired_samplesize:    
        print 'x/n total users collected so far. Collecting the next batch of 100 users'
        call batch_data_collection function
        print 'Pausing for x seconds' 
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
        # print('User ids collected: '+str(data.user_ids_collected))
        # this is the time window when we can interrupt batch_data_collection 
        # NB I've chosen 10 seconds sleep, slightly arbitrarily, based on experiments so far
        time.sleep(pause_between_batches) # wait 10 seconds to give the server a break
        print 'Finished pausing, time for more data collection - please do not interrupt...'
    print('Snowball sample fully collected with a sample size of '+str(len(data.user_ids_collected))+' users. Saving a copy of the data to scdb_final.sqlite')
    export_data_to_SQLite(data,'scdb_final.sqlite')
    data.print_data_summary()
    return data # in case results are to be collected during runtime  


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
	        call collect_follows_and_followers_data(user)
	        call collect_favourited_tracks_data(user)
	        call collect_groups_data(user)
	        call collect_produced_tracks_data(user)
	        call collect_comments_data(user)
	        call collect_playlist_data(user)
		# now finished with this user, move onto the next user until 100 users collected
		num_users_collected++
	# (go back to the start of the repeat loop again)
	
	# Now we have collected 100 users
	call backup_and_save_data and save collected data externally
	# done
	'''
    # repeat until 100 users collected:
    num_users_to_be_collected = len(data.user_ids_collected)+batch_size
    
    while(len(data.user_ids_collected) < num_users_to_be_collected):
#        if the user_ids_to_collect set is nonempty:      
#            pop a user_id from the set and set that user_id as seed.
        seed_user_found = False
        potential_new_seed_user = 0 # init dummy value
        while ((len(data.user_ids_to_collect) > 0) and not(seed_user_found)):
            potential_new_seed_user = data.user_ids_to_collect.pop()
            # check data hasn't already been collected for this new seed user (just in case)
            seed_user_found = not(potential_new_seed_user in data.user_ids_collected)
            # (if it has been, go round the inner while loop again till either 
            # there are no more user_ids_to_collect or till a new seed user has been found 
        if (seed_user_found):
            seed_user = client_get('/users/'+str(potential_new_seed_user))
            seed_user_id = potential_new_seed_user
        # else: set random user as seed
        else: 
            seed_user = get_random_user()
            seed_user_id = seed_user.id

        data.users.add(convert_soundcloud_resource_for_data(seed_user, 'users'))
        data.user_ids_collected.add(seed_user_id)
       
        # Collect data relevant to that user
        # NB 'collect'='get data from soundcloud API, store in relevant internal data structure'
        # if an item has already been collected, collect it again and check if 
        # the collected info needs updating 
        # (we want to have the most up to date information)
        collect_follows_and_followers_data(data, seed_user_id)
        collect_favourited_tracks_data(data, seed_user_id)
        collect_groups_data(data, seed_user_id)
        collect_produced_tracks_data(data, seed_user_id)
        collect_comments_data(data, seed_user_id)
        collect_playlist_data(data, seed_user_id)
        # now finished with this user, move onto the next user until 100 users collected
        # (go back to the start of the repeat loop again)
    
    # Here we are out of the while loop - we have collected 100 users
    backup_and_save_data(data)
    # done
    

def deal_with_new_user(data, user_id):
    ''' Check to see if we have already collected data on this user in previous data collection,
        or if we are already planning to collect data on this user. 
        If neither of these cases are true, add the user's id to the set of 
        user ids to be collected in future data_collection '''
    # Check, user_id can't be in either list
    if (not(user_id in data.user_ids_to_collect) and not(user_id in data.user_ids_collected)):
        data.user_ids_to_collect.add(user_id)
        
def deal_with_new_track(data, track_id, track_object=None):        
    ''' Check to see if we have already collected data on this track in previous data collection.
        If we haven't collected this data already, collect it and add to the tracks data '''
    # check to see if we have already collected the track in previous data collection
    if (not(track_id in data.track_ids_collected)):
        if (track_object==None):   # get the track, if we haven't already gotten it from API
            track_object = client_get('/tracks/'+str(track_id))
        # before saving the track to our data, we want to extract one 
        # sub attribute of the track's attributes and add it as a top-level att.
        # (Doing this now makes it easy to save the data to DB later)
        # This is for the 'permalink_url' info relating to the app that 
        # was used to create this track (if one was used)
        if (not(track.created_with==None)):
            try:
                track.created_using_permalink_url = track.created_with['permalink_url']
            except: # if this info is missing, ignore this for now 
                pass
                # (as any missing attributes will be dealt with later) 
        # Now we're ready to add the new track to our data
        data.tracks.add(convert_soundcloud_resource_for_data(track_object, 'tracks'))
        data.track_ids_collected.add(track_id)
        # add track_producer_id to user_ids_to_collect
        deal_with_new_user(data, track_object.user_id)
    
def deal_with_new_comment(data, comment):
    ''' Check to see if we have already collected data on this comment in previous data collection.
        If we haven't collected this data already, collect it and add to the comments data '''
    if (not(comment.id in data.comment_ids_collected)):
        data.comments.add(convert_soundcloud_resource_for_data(comment, 'comments'))
        # add comment id to comment_ids_collected
        data.comment_ids_collected.add(comment.id)
        # collect user id and add to user_ids_to_be_collected if not already collected
        deal_with_new_user(data, comment.user_id)
    # else do nothing, comment already collected and process


def collect_follows_and_followers_data(data, user):
    '''collect ids of all users that our seed user follows: 
 		construct follows relationship tuple for each follow (seed_id, followed_user_id)
		add ids to user_ids_to_collect
       then collect ids of all users that follow our seed user:
		construct follows relationship tuple for each follow (follower_user_id, seed_id)
		add ids to user_ids_to_collect
    '''
    # collect ids of all users that our seed user follows 
    # (all 'followings' of a user, in SC speak)    
    followings = client_get('/users/'+str(user)+'/followings')
    for following in followings:
        # construct follows relationship tuple for each following (seed_id, followed_user_id)
        data.x_follows_y.add((user, following.id))
        # Add the followed user to add ids to user_ids_to_collect (if not already collected) 
        deal_with_new_user(data, following.id)
            
    # then collect ids of all users that follow our seed user: 
    followers = client_get('/users/'+str(user)+'/followers')
    for follower in followers:
        # construct follows relationship tuple for each follow (follower_user_id, seed_id)
        data.x_follows_y.add((follower.id, user))
        # add the follower user to user_ids_to_collect (if not already collected)
        deal_with_new_user(data, follower.id)
      

    
def collect_favourited_tracks_data(data, user):
    ''' collect all the user's favourited tracks
		construct favourites tuple for each favouriting: (user_id, track_id, track_producer_id)
		collect track information and add track_id to track_ids_collected
		add all track_producer_ids to user_ids_to_collect
    '''
    # collect all the user's favourited tracks
    user_favourites = client_get('/users/'+str(user)+'/favorites') # Remember US spelling
    for fave in user_favourites:
        # construct favourites tuple for each favouriting: 
        # (our_favouriting_user_id, track_id, track_producer_id)
        data.favourites.add((user,fave.id,fave.user_id))
        # collect track information and add track_id to track_ids_collected
        deal_with_new_track(data, str(fave.id))

        
        
def collect_groups_data(data, user): 
    ''' collect all the user's groups
		construct tuple (seed_user_id, group_id) for group_mem table
		add group to the groups table
    '''
######################## We can get this information about groups:
######################## [u'permalink', u'members_count', u'name', u'track_count', u'creator', 
########################  u'artwork_url', u'created_at', u'kind', u'uri', u'moderated', 
########################  u'short_description', u'contributors_count', u'permalink_url', 
########################  u'id', u'description']

    # collect all the user's groups
    user_groups = client_get('/users/'+str(user)+'/groups')
    # construct tuple (seed_id, group_id, group_name)
    for group in user_groups:
        data.group_mem.add((user, group.id))
        # NB a group is created by a user. 
        # So we add group_creator_id to user_ids_to_collect and collect info on the group
        # joining a group could be a measure of influence of the *creator* of the group
        # NB Some groups don't have a creator - check
        if (not(group.creator == None)): 
            deal_with_new_user(data, group.creator['id'])
            # before saving the track to our data, we want to extract one 
            # sub attribute of the track's attributes and add it as a top-level att.
            # (Doing this now makes it easy to save the data to DB later)
            # This is for the 'permalink_url' info relating to the app that 
            # was used to create this track (if one was used)
            try:
                group.creator_id = group.creator['id']
            except: # if this info is missing, ignore this for now 
                pass
                    # (as any missing attributes will be dealt with later) 
        # Now we're ready to add the new group info to our data (if not already added)
        if (not(group.id in data.group_ids_collected)):
            data.groups.add(convert_soundcloud_resource_for_data(group, 'groups'))
            data.group_ids_collected.add(group.id)

 
def collect_produced_tracks_data(data, user):
    ''' collect all tracks produced by seed user
	 for each track:
		collect all comments made on seed user's tracks
		for each comment collected on seed user's track:
			add comment id to comment_ids_collected
			collect user id and add to user_ids_to_be_collected
    ''' 
    # collect all tracks produced by seed user
    user_tracks = client_get('/users/'+str(user)+'/tracks')
    # for each track:
    for track in user_tracks:
        deal_with_new_track(data, track.id, track)
        # collect all comments made on seed user's tracks
        # NB Comments aren't dynamic in the same way as tracks, 
        # so we don't need to be so vigilant about collecting the most up to date version
        comments_on_track = client_get('/tracks/'+str(track.id)+'/comments')
#        for each comment collected on seed user's track:
        for comment in comments_on_track:
            deal_with_new_comment(data, comment)


def collect_comments_data(data, user):
    ''' collect all comments made by seed user
    for each comment:
		add comment id to comment_ids_collected
		collect track information and add track id to track_ids_collected
		add track_creator_id to user_ids_to_collect
    '''
    # collect all comments made by seed user
    user_comments = client_get('/users/'+str(user)+'/comments')
    for comment in user_comments:
        deal_with_new_comment(data, comment)
        # collect track information and deal with new track
        deal_with_new_track(data, comment.track_id)
        
        
def collect_playlist_data(data, user):
    '''	collect all playlists by the user
		construct playlist tuple for each playlisted track: (user_id, playlist_id,track_id, track_producer_id)
		collect track information and add track_id to track_ids_collected
		add all track_producer_ids to user_ids_to_collect 
    ''' 
    
    # collect all playlists by the user
    user_playlists = client_get('/users/'+str(user)+'/playlists') 
    for playlist in user_playlists: # each playlist has a list of tracks
        for track in playlist.tracks: # each track on a playlist is represented as a dict object
            # construct playlist tuple for each playlisted track: 
            # (user_id, playlist_id,track_id, track_producer_id)
            data.playlists.add((user,playlist.id,track['id'],track['user_id']))
            deal_with_new_track(data, track['id'])




def backup_and_save_data(data):
    '''
        backup: (grandfather - father - son: grandfather is the oldest backup,
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
    print('TODO backup_and_save_data')
    # TODO possibly put this within SC_data class?
 
    # use export_data_to_SQLite
    # and
    # https://docs.python.org/2/library/os.html
    # and 
    # pickle.dump(current_ids, open("current_ids.p", "wb"))
    
    export_data_to_SQLite(data, db_path)
    print('Latest snapshot of data stored in '+db_path+' database.')





def export_data_table(cursor, table_data, table_name):
    print ('Creating '+table_name+' table in DB....')
    ad.create_table(cursor, table_name)
    ad.insert_tuple_data_set_into_DB(cursor, table_name, table_data)
    

def export_data_to_SQLite(data, db_path):
#    print '' # for neater display 
    try:
        db = sqlite3.connect(db_path)
        cursor = db.cursor()

        export_data_table(cursor, data.users, 'users')
        export_data_table(cursor, data.x_follows_y, 'x_follows_y')
        export_data_table(cursor, data.tracks, 'tracks')
        export_data_table(cursor, data.groups, 'groups')
        export_data_table(cursor, data.group_mem, 'group_mem')
        export_data_table(cursor, data.favourites, 'favourites')
        export_data_table(cursor, data.comments, 'comments')
        export_data_table(cursor, data.playlists, 'playlists')
        
        # TODO currently included for completeness 
        # though the tables are only going to be empty sets at present
        export_data_table(cursor, data.genres, 'genres')
        export_data_table(cursor, data.tags, 'tags')
        export_data_table(cursor, data.user_genres, 'user_genres')
        export_data_table(cursor, data.user_tags, 'user_tags')
        export_data_table(cursor, data.x_faves_work_of_y, 'x_faves_work_of_y')
        export_data_table(cursor, data.comments_corp, 'comments_corp')
         
#         for group in groups:
#             try:
#                 cursor.execute('''INSERT INTO group_mem(id, members_count, name, track_count, creator_id, created_at, uri, moderated, short_description, contributors_count, description) 
#                               VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
#                               (group.id, group.members_count, group.name, group.track_count, group.creator['id'], group.created_at, group.uri, group.moderated, group.short_description, group.contributors_count, group.description))
#             except Exception as e:
#                 print('Error adding group '+str(group.id)+' to the database: '+e.message+' '+str(e.args))


        print 'Ready to commit DB to file'
        db.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        print 'Exception caught in export_data_to_SQLite function'
        print e.message
        print(str(e.args))
        #raise e
    finally:
        # Close the db connection
        db.close()
        print('Data saved in '+db_path)


def main(requested_sample_size = 10, requested_batch_size=2): 
    print('starting')
    seed = set([80778799])
    sample = get_new_snowball_sample(sample_size=requested_sample_size, desired_seed_users = seed, batch_size=requested_batch_size)
    print 'finished'  
    #printData() 
    #export_data_to_SQLite()

if __name__ == '__main__':
    main(requested_sample_size=0)