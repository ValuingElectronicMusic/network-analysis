'''
Created on June 30th, 2014

@author: annajordanous
'''
import random
import soundcloud  
import get_soundcloud_data as gsc
import process_scdb_data as pscd
import time
import sqlite3

def connect_to_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return cursor

def run_sql_query(cursor, query):
   
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def get_track_creator(track_id):
    query = 'SELECT user_id FROM tracks WHERE id = '+track_id
    return run_sql_query(query)

def main(db_path): 
#    data = pscd.data_holder(db_path)
#    pscd.printData(data)
#    entities = pscd.entity_holder(data)
#    pscd.printEntities(entities)
    cursor = connect_to_db(db_path)
    result = run_sql_query(cursor, 'SELECT COUNT(*) from users')
    print(result)
 

if __name__ == '__main__':
    main('scdb_FINAL.sqlite')