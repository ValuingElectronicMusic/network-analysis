'''
Created on June 30th, 2014

@author: annajordanous
'''

import sqlite3

def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor

def run_sql_query(cursor, query):
   
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_track_creator(cursor, track_id):
    query = 'SELECT user_id FROM tracks WHERE id = '+str(track_id)
    return run_sql_query(cursor, query)

def get_all_connections_for_user(cursor, user_id):
    ''' Demonstration of all the methods available in this file for getting information on connections to and from a given user'''
    
    connections = dict()
    
    try:
        print('Finding FOLLOWS (users) relationships for user '+str(user_id))
    
        num_users = get_num_users_this_user_follows(cursor, user_id)
        print('Number of users this user follows: '+str(num_users))
        connections['num_users_this_user_follows'] = num_users
    
        list_users = get_users_this_user_follows(cursor, user_id)  
        print('List of users this user follows: '+str(list_users))
        connections['list_users_this_user_follows'] = list_users
    
        num_users = get_num_users_following_this_user(cursor, user_id)  
        print('Number of users who follow this user: '+str(num_users))
        connections['num_users_following_this_user'] = num_users
    
        list_users = get_users_following_this_user(cursor, user_id)  
        print('List of users who follow this user: '+str(list_users))
        connections['list_users_following_this_user'] = list_users
    except Exception as e:
        print('Could not collect FOLLOWS relationships for this user: '+e.message+str(e.args))

    try:
        print('Finding LIKES (tracks) relationships for user '+str(user_id))
    
        num_users = get_num_users_this_user_likes_tracks_of(cursor, user_id)
        print('Number of users whose tracks this user has liked: '+str(num_users))
        connections['num_users_this_user_likes_tracks_of'] = num_users
    
        list_users = get_users_this_user_likes_tracks_of(cursor, user_id)
        print('List of users whose tracks this user has liked: '+str(list_users))
        connections['list_users_this_user_likes_tracks_of'] = list_users
    
        num_users = get_num_users_liking_this_users_tracks(cursor, user_id)
        print('Number of users who have liked this users tracks: '+str(num_users))
        connections['num_users_liking_this_users_tracks'] = num_users
    
        list_users = get_users_liking_this_users_tracks(cursor, user_id)
        print('List of users who have liked this users tracks: '+str(list_users))
        connections['list_users_liking_this_users_tracks'] = list_users
    except Exception as e:
        print('Could not collect LIKES relationships for this user: '+e.message+str(e.args))

    try:    
        print('Finding COMMENTING relationships for user '+str(user_id))
        
        num_users = get_num_users_this_user_commented_on_tracks_for(cursor, user_id)
        print('Number of users whose tracks this user has commented on: '+str(num_users))
        connections['num_users_this_user_has_commented_on_tracks'] = num_users
    
        list_users = get_users_this_user_commented_on_tracks_for(cursor, user_id)
        print('List of users whose tracks this user has commented on: '+str(list_users))
        connections['list_users_this_user_has_commented_on_tracks'] = list_users
    
        num_users = get_num_users_commenting_on_this_users_tracks(cursor, user_id)
        print('Number of users who have commented on this users tracks: '+str(num_users))
        connections['num_users_commenting_on_this_users_tracks'] = num_users
    
        list_users = get_users_commenting_on_this_users_tracks(cursor, user_id)
        print('List of users who have commented on this users tracks: '+str(list_users))
        connections['list_users_commenting_on_this_users_tracks'] = list_users
    except Exception as e:
        print('Could not collect COMMENTING relationships for this user: '+e.message+str(e.args))

    try:
        print('Finding PLAYLIST-based relationships for user '+str(user_id))
    
        num_users = get_num_users_this_user_playlisted_tracks_of(cursor, user_id)
        print('Number of users who this user has playlisted tracks of: '+str(num_users))
        connections['num_users_this_user_playlisted_tracks_of'] = num_users
    
        list_users = get_users_this_user_playlisted_tracks_of(cursor, user_id)
        print('List of users who this user has playlisted tracks of: '+str(list_users))
        connections['list_users_this_user_playlisted_tracks_of'] = list_users
    
        num_users = get_num_users_playlisting_this_user_tracks(cursor, user_id)
        print('Number of users who have playlisted this users tracks: '+str(num_users))
        connections['num_users_playlisting_this_users_tracks'] = num_users
    
        list_users = get_users_playlisting_this_user_tracks(cursor, user_id)
        print('List of users who have playlisted this users tracks: '+str(list_users))
        connections['list_users_playlisting_this_users_tracks'] = list_users
    except Exception as e:
        print('Could not collect PLAYLIST-based relationships for this user: '+e.message+str(e.args))

    try:
        print('Finding GROUP-based relationships for user '+str(user_id))
    
        num_users = get_num_users_in_this_users_groups(cursor, user_id) 
        print('Number of users in groups created by this user: '+str(num_users))
        connections['num_users_in_groups_created_by_this_user'] = num_users
    
        list_users = get_users_in_this_users_groups(cursor, user_id)
        print('List of users in this users groups: '+str(list_users))
        connections['list_users_in_groups_created_by_this_user'] = list_users
    
        num_users = get_num_creators_of_groups_this_user_is_in(cursor, user_id)
        print('Number of users creating groups that this user is in: '+str(num_users))
        connections['num_users_creating_this_users_groups'] = num_users
    
        list_users = get_creators_of_groups_this_user_is_in(cursor, user_id)
        print('List of users creating groups that this user is in: '+str(list_users))
        connections['list_users_creating_this_users_groups'] = list_users
    except Exception as e:
        print('Could not collect GROUP-based relationships for this user: '+e.message+str(e.args))

 
    return connections

###################################################
# Queries for which users this given user follows #
###################################################
def get_num_users_this_user_follows(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT followed) ' 
                         +'FROM x_follows_y ' 
                         +'WHERE follower='+str(user_id))
    return num_users[0][0]

def get_users_this_user_follows(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT followed ' 
                         +'FROM x_follows_y ' 
                         +'WHERE follower='+str(user_id))
    return {x[0] for x in users}

##################################################
# Queries for which users follow the given users #
##################################################
def get_num_users_following_this_user(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT follower) ' 
                         +'FROM x_follows_y ' 
                         +'WHERE followed='+str(user_id))
    return num_users[0][0]

def get_users_following_this_user(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT follower ' 
                         +'FROM x_follows_y ' 
                         +'WHERE followed='+str(user_id))
    return {x[0] for x in users}

#########################################################################
# Queries for which users have had tracks favourited by the given users #
#########################################################################
def get_num_users_this_user_likes_tracks_of(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT track_producer_id) ' 
                         +'FROM favourites ' 
                         +'WHERE user_id='+str(user_id))
    return num_users[0][0]

def get_users_this_user_likes_tracks_of(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT track_producer_id ' 
                         +'FROM favourites ' 
                         +'WHERE user_id='+str(user_id))
    return {x[0] for x in users}

###################################################################
# Queries for which users have favourited the given user's tracks #
###################################################################
def get_num_users_liking_this_users_tracks(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT user_id) ' 
                         +'FROM favourites ' 
                         +'WHERE track_producer_id='+str(user_id))
    return num_users[0][0]

def get_users_liking_this_users_tracks(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT user_id ' 
                         +'FROM favourites ' 
                         +'WHERE track_producer_id='+str(user_id))
    return {x[0] for x in users}

##################################################################
# Queries for which users have tracks this user has commented on #
##################################################################
def get_num_users_this_user_commented_on_tracks_for(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT tracks.user_id) ' 
                         +'FROM comments JOIN tracks ' 
                         +'WHERE comments.track_id = tracks.id '
                         +'AND comments.user_id='+str(user_id))
    return num_users[0][0]

def get_users_this_user_commented_on_tracks_for(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT tracks.user_id ' 
                         +'FROM comments JOIN tracks ' 
                         +'WHERE comments.track_id = tracks.id '
                         +'AND comments.user_id='+str(user_id))
    return {x[0] for x in users}

###############################################################
# Queries for which users have commented on this users tracks #
###############################################################
def get_num_users_commenting_on_this_users_tracks(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT comments.user_id) ' 
                         +'FROM comments JOIN tracks ' 
                         +'WHERE comments.track_id = tracks.id '
                         +'AND tracks.user_id='+str(user_id))
    return num_users[0][0]

def get_users_commenting_on_this_users_tracks(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT comments.user_id ' 
                         +'FROM comments JOIN tracks ' 
                         +'WHERE comments.track_id = tracks.id '
                         +'AND tracks.user_id='+str(user_id))
    return {x[0] for x in users}

#########################################################################
# Queries for which users have had tracks playlisted by the given users #
#########################################################################
def get_num_users_this_user_playlisted_tracks_of(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT user_id) ' 
                         +'FROM playlists ' 
                         +'WHERE track_producer_id='+str(user_id))
    return num_users[0][0]

def get_users_this_user_playlisted_tracks_of(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT user_id ' 
                         +'FROM playlists ' 
                         +'WHERE track_producer_id='+str(user_id))
    return {x[0] for x in users}

###################################################################
# Queries for which users have playlisted the given user's tracks #
###################################################################
def get_num_users_playlisting_this_user_tracks(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT track_producer_id) ' 
                         +'FROM playlists ' 
                         +'WHERE user_id='+str(user_id))
    return num_users[0][0]

def get_users_playlisting_this_user_tracks(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT track_producer_id ' 
                         +'FROM playlists ' 
                         +'WHERE user_id='+str(user_id))
    return {x[0] for x in users}

##########################################################
# Queries for who is in groups created by the given user #
##########################################################
def get_num_users_in_this_users_groups(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT group_mem.user_id) ' 
                         +'FROM groups JOIN group_mem ' 
                         +'WHERE groups.id=group_mem.group_id '
                         +'AND groups.creator_id='+str(user_id))
    return num_users[0][0]

def get_users_in_this_users_groups(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT group_mem.user_id ' 
                         +'FROM groups JOIN group_mem ' 
                         +'WHERE groups.id=group_mem.group_id '
                         +'AND groups.creator_id='+str(user_id))
    return {x[0] for x in users}

#########################################################
# Queries for who created the groups a given user is in #
#########################################################
def get_num_creators_of_groups_this_user_is_in(cursor, user_id):
    num_users = run_sql_query(cursor, 
                         'SELECT COUNT(DISTINCT groups.creator_id) ' 
                         +'FROM groups JOIN group_mem ' 
                         +'WHERE groups.id=group_mem.group_id '
                         +'AND group_mem.user_id='+str(user_id))
    return num_users[0][0]

def get_creators_of_groups_this_user_is_in(cursor, user_id):
    users = run_sql_query(cursor, 
                         'SELECT DISTINCT groups.creator_id ' 
                         +'FROM groups JOIN group_mem ' 
                         +'WHERE groups.id=group_mem.group_id '
                         +'AND group_mem.user_id='+str(user_id))
    return {x[0] for x in users}

def get_all_connections_between_two_users(cursor, user_id1, user_id2):
    ''' Demonstration of all the methods available in this file for getting information on connections between two given users'''
    print('Finding relationships between the SoundCloud users '+str(user_id1)+' and '+str(user_id2))
    connections = dict()
    try:
        if run_sql_query(cursor, 'SELECT count(followed) from x_follows_y WHERE follower='+str(user_id1))==1:
            print(str(user_id1)+' follows '+str(user_id2))
            u1_follows_u2 = True
        else: 
            print(str(user_id1)+' does not follow '+str(user_id2))
            u1_follows_u2 = False
        connections['u1_follows_u2'] = u1_follows_u2
        if run_sql_query(cursor, 'SELECT count(followed) from x_follows_y WHERE follower='+str(user_id2))==1:
            print(str(user_id2)+' follows '+str(user_id1))
            u2_follows_u1 = True
        else: 
            print(str(user_id2)+' does not follow '+str(user_id1))
            u2_follows_u1 = False
        connections['u2_follows_u1'] = u2_follows_u1
    except Exception as e:
        print('Could not collect FOLLOWS relationships between these users: '+e.message+str(e.args))

    try:
        u1_likes_u2_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(track_id) FROM favourites '
                                           +'WHERE user_id = '+str(user_id1)+' AND track_producer_id = '+str(user_id2))[0][0]
        print('User '+str(user_id1)+' likes '+str(u1_likes_u2_tracks)+' tracks by '+str(user_id2))
        connections['u1_likes_u2_tracks'] = u1_likes_u2_tracks
        u2_likes_u1_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(track_id) FROM favourites '
                                           +'WHERE user_id = '+str(user_id2)+' AND track_producer_id = '+str(user_id1))[0][0]
        print('User '+str(user_id2)+' likes '+str(u2_likes_u1_tracks)+' tracks by '+str(user_id1))
        connections['u2_likes_u1_tracks'] = u2_likes_u1_tracks
    except Exception as e:
        print('Could not collect LIKES relationships between these users: '+e.message+str(e.args))

    try:
        u1_comments_on_u2_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(comments.id) FROM comments JOIN tracks '
                                           +'WHERE comments.track_id = tracks.id '
                                           +'AND comments.user_id = '+str(user_id1)
                                           +' AND tracks.user_id = '+str(user_id2))[0][0]
        print('User '+str(user_id1)+' has made '+str(u1_comments_on_u2_tracks)+' comments on tracks by '+str(user_id2))
        connections['u1_comments_on_u2_tracks'] = u1_comments_on_u2_tracks
        u2_comments_on_u1_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(comments.id) FROM comments JOIN tracks '
                                           +'WHERE comments.track_id = tracks.id '
                                           +'AND comments.user_id = '+str(user_id2)
                                           +' AND tracks.user_id = '+str(user_id1))[0][0]
        print('User '+str(user_id2)+' has made '+str(u2_comments_on_u1_tracks)+' comments on tracks by '+str(user_id1))
        connections['u2_comments_on_u1_tracks'] = u2_comments_on_u1_tracks
    except Exception as e:
        print('Could not collect COMMENTING relationships between these users: '+e.message+str(e.args))

    try:
        u1_playlists_u2_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(track_id) FROM playlists '
                                           +'WHERE user_id = '+str(user_id1)+' AND track_producer_id = '+str(user_id2))[0][0]
        print('User '+str(user_id1)+' has playlisted '+str(u1_playlists_u2_tracks)+' tracks by '+str(user_id2))
        connections['u1_playlists_u2_tracks'] = u1_playlists_u2_tracks
    
        u2_playlists_u1_tracks = run_sql_query(cursor, 
                                           'SELECT COUNT(track_id) FROM playlists '
                                           +'WHERE user_id = '+str(user_id2)+' AND track_producer_id = '+str(user_id1))[0][0]
        print('User '+str(user_id2)+' has playlisted '+str(u2_playlists_u1_tracks)+' tracks by '+str(user_id1))
        connections['u2_playlists_u1_tracks'] = u2_playlists_u1_tracks
    except Exception as e:
        print('Could not collect PLAYLIST-based relationships between these users: '+e.message+str(e.args))

    try:
        u1_in_u2_groups = run_sql_query(cursor, 
                                           'SELECT COUNT(group_mem.group_id) FROM group_mem JOIN groups '
                                           +'WHERE group_mem.group_id = groups.id '
                                           +'AND group_mem.user_id = '+str(user_id1)
                                           +' AND groups.creator_id = '+str(user_id2))[0][0]
        print('User '+str(user_id1)+' is in '+str(u1_in_u2_groups)+' groups created by '+str(user_id2))
        connections['u1_in_u2_groups'] = u1_in_u2_groups
        u2_in_u1_groups = run_sql_query(cursor, 
                                           'SELECT COUNT(group_mem.group_id) FROM group_mem JOIN groups '
                                           +'WHERE group_mem.group_id = groups.id '
                                           +'AND group_mem.user_id = '+str(user_id2)
                                           +' AND groups.creator_id = '+str(user_id1))[0][0]
        print('User '+str(user_id2)+' is in '+str(u2_in_u1_groups)+' groups created by '+str(user_id1))
        connections['u2_in_u1_groups'] = u2_in_u1_groups
    except Exception as e:
        print('Could not collect GROUP-based relationships between these users: '+e.message+str(e.args))
    
    return connections
   

def main(db_path, user_id1 = 117854, user_id2 = 104353): 
    print('Analysing connections between users. Warning, for large data this may take some time to run.')
    cursor = connect_to_db(db_path)
    #print(get_all_connections_for_user(cursor, user_id1)) 
    print(get_all_connections_between_two_users(cursor, user_id1, user_id2))
    
if __name__ == '__main__':
    main('scdb_FINAL.sqlite')
