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
   
    curs.execute(query)
    result = curs.fetchall()
    return result


def main(db_path): 
    data = pscd.data_holder(db_path)
    pscd.printData(data)
    entities = pscd.entity_holder(data)
    pscd.printEntities(entities)
 

if __name__ == '__main__':
    main('scdb_FINAL.sqlite')