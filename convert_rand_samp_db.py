import sqlite3
import add_data

def rename_old_sample_table(curs):
    curs.execute('ALTER TABLE sample RENAME TO ids_tried')

def create_new_sample_table(curs):
    curs.execute('CREATE TABLE sample (id INTEGER PRIMARY KEY)')

def rename_old_tracks_table(curs):
    curs.execute('ALTER TABLE tracks RENAME TO old_tracks')

def create_new_tracks_table(curs):
    add_data.create_table(curs,'tracks')

def get_tracks_data(curs):
    curs.execute('SELECT * FROM old_tracks')
    data=curs.fetchall()
    print 'Got data. Now to write it...'
    return data
'''    return [(d[0],int(d[1]))+d[2:] for d in data]'''

def write_tracks_data(curs,data):
    sql='INSERT INTO tracks VALUES ({})'.format(','.join(['?']*40))
    curs.executemany(sql,data)

def get_sample(curs):
    curs.execute('SELECT id FROM ids_tried')
    ids_tried = set(curs.fetchall())
    print 'Got the set of user id numbers tried'
    sample=[]
    for n,id in enumerate(curs.execute('SELECT id FROM users')):
        if id in ids_tried: sample.append(id)
        if n % 1000 == 0: 
            print ('{} users scanned '
                   '{} users in sample found'.format(n,len(sample)))
    return sample

def write_sample(curs,data):
    curs.executemany('INSERT INTO sample(id) VALUES(?)',data)

def sort_out_sample(curs):
    '''    rename_old_sample_table(curs)
    create_new_sample_table(curs)'''
    samp=get_sample(curs)
    write_sample(curs,samp)

def sort_out_tracks(curs):
    '''    rename_old_tracks_table(curs)
    create_new_tracks_table(curs)'''
    print 'Tables changed. Now for the data...'
    write_tracks_data(curs,get_tracks_data(curs))

def convert_db(db_path):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    '''    print 'Starting work on tracks...'
    sort_out_tracks(curs)
    conn.commit()
    print 'Tracks done.' '''
    sort_out_sample(curs)
    conn.commit()
    print 'Sample done.'
