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
    num_users_this_user_follows = 0
    num_users_following_this_user = 0
    num_users_this_user_likes_tracks_of = 0
    num_users_liking_this_users_tracks = 0
    num_users_this_user_commented_on_tracks_for = 0
    num_users_commenting_on_this_users_tracks = 0
    num_users_this_user_playlisted_tracks_of = 0
    num_users_playlisting_this_users_tracks = 0
    print(get_num_users_in_this_users_groups(cursor, user_id))
    num_users_with_groups_this_user_is_in = 0

def get_num_users_in_this_users_groups(cursor, user_id):
    return run_sql_query(cursor, 
                         'SELECT COUNT(group_mem.user_id)' 
                         +'FROM groups INNER JOIN group_mem ON groups.id=group_mem.group_id '
                         +'WHERE groups.creator_id='+str(user_id))
def main(db_path): 
#    data = pscd.data_holder(db_path)
#    pscd.printData(data)
#    entities = pscd.entity_holder(data)
#    pscd.printEntities(entities)
    cursor = connect_to_db(db_path)
#    print(run_sql_query(cursor, 'SELECT COUNT(*) from users'))
#    print(get_track_creator(cursor, 136))
    #print(run_sql_query(cursor, 'SELECT creator_id FROM groups'))
    user_id = 13128
    print(get_all_connections_for_user(cursor, user_id)) 

if __name__ == '__main__':
    main('scdb_FINAL.sqlite')