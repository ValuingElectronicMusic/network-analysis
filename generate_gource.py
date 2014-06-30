'''
Created on 19 May 2014

@author: annaj
'''
import sqlite3
import time
#from email.utils import parsedate_tz
from calendar import timegm
import string
import random 

#comments_table_creator='''id INTEGER PRIMARY KEY, user_id INTEGER, track_id INTEGER, 
# body TEXT, timestamp INTEGER, created_at TEXT, uri TEXT'''

# tracks_table_creator='''id INTEGER PRIMARY KEY, user_id TEXT,  
# title TEXT, permalink_url TEXT, description TEXT, tag_list TEXT, state TEXT,
# duration INTEGER, genre TEXT,  key_signature TEXT, bpm INTEGER,  
# original_content_size INTEGER, original_format TEXT, track_type TEXT,    
# sharing TEXT, streamable TEXT, embeddable_by TEXT, downloadable TEXT, commentable TEXT,
# release INTEGER, release_year INTEGER, release_month INTEGER, release_day INTEGER,
# purchase_title TEXT, purchase_url TEXT, label_id TEXT, label_name TEXT, license TEXT, 
# isrc TEXT, video_url TEXT, artwork_url TEXT, 
# waveform_url TEXT, stream_url TEXT, attachments_uri TEXT,
# playback_count INTEGER, download_count INTEGER, 
# favoritings_count INTEGER, comment_count INTEGER, 
# created_at TEXT, created_using_permalink_url TEXT'''

def get_comments_data(db_name):
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()
    curs.execute("SELECT comments.created_at, users.username, 'M', comments.track_id, tracks.user_id FROM comments JOIN tracks JOIN users where comments.track_id = tracks.id and tracks.user_id = users.id")
    list_of_comments = curs.fetchall()  # list returned by curs.fetchall()
    track_interactions = list_of_comments
    tracks = {comment[3] for comment in list_of_comments}
    for track_id in tracks:
        curs.execute("SELECT tracks.created_at, users.username, 'A', tracks.id, tracks.user_id FROM tracks JOIN users WHERE tracks.user_id = users.id and tracks.id="+str(track_id))
        results = curs.fetchall()
        track_interactions.append(results[0])
    conn.close()
    
    track_interactions.sort()
    return track_interactions

def convert_comment(comment):
    #discard any comments without timestamp (for now)
    if (comment[0] == None or comment[0] <= 0):
        return ''
    else:
    #Convert created_at timestamp to unix timestamp, as required for gource
        try:
            timestamp = timegm(time.strptime(comment[0], "%Y/%m/%d %H:%M:%S +0000"))
        except ValueError as ve:
            print(comment[0]+' - value error - '+str(ve))
            
            # maybe a different timezone 
#             if ('+' in comment[0] or '-' in comment[0]):
#                 if ('+' in comment[0]):
#                     split_time_and_timezone = string.rsplit(comment[0], '+', 1)
#                     multiplier = 1
#                 else: 
#                     split_time_and_timezone = string.rsplit(comment[0], '-', 1)
#                     multiplier = -1
#                 split_time = time.strptime(split_time_and_timezone[0], "%Y/%m/%d %H:%M:%S ")
#                 timezone = int(int(split_time_and_timezone[1])/100) * multiplier 
#                 split_time.tm_hour = split_time.tm_hour + timezone
#                 timestamp = timegm(split_time)

            # but just ignore different timezone for now - life is too short! TODO
            if ('+' in comment[0]):
                split_time_and_timezone = string.rsplit(comment[0], '+', 1)
            else:
                if ('-' in comment[0]):
                    split_time_and_timezone = string.rsplit(comment[0], '-', 1)
                else: 
                    return ''
#                    multiplier = -1
            timestamp = timegm(time.strptime(split_time_and_timezone[0], "%Y/%m/%d %H:%M:%S "))

        except Exception as e:
            print(comment[0]+' - exception - '+str(e))
            return ''         
        # return str(int(timestamp))+'|'+str(comment[1])+'|'+str(comment[2])+'|'+str(comment[3])+'|'+str(hex(timestamp % 0xFFFFFF))[2:]+'\n'
#         return_string timestamp |  username | type  |  path of track, as user/trackid (to get best clusters of a user)  | random_colour
#         if (comment[2] == 'A'):
#             return str(int(timestamp))+'|'+lower_case_str(comment[1])+'|'+comment[2]+'|'+comment[1]+'/'+str(comment[3])+'|'+str(hex(random.randint(0,0xFFFFCC)))[2:]+'\n'
#         else: 
        return_string = str(int(timestamp))
        return_string = return_string+'|'+lower_case_str(comment[1])
        return_string = return_string+'|'+str(comment[2])
        return_string = return_string+'|'+str(comment[4])
        return_string = return_string+'/'+str(comment[3])
        return_string = return_string+'|'+str(hex(random.randint(0,0xFFFFCC)))[2:]+'\n'
        return return_string
          
def lower_case_str(inputText):
    return str.lower(unicode(inputText).encode('utf-8'))
    
def generate_gource_log(comments):
    gource_log = ''
    for comment in comments:
        converted_comment = convert_comment(comment)
        gource_log += converted_comment
    return gource_log

def main(db_name='seed_81070_20140602_1852.sqlite'):
    gource_log = generate_gource_log(get_comments_data(db_name))
    gource_logfile = open('gource.log', 'w')
    gource_logfile.write(gource_log) 
    gource_logfile.close()

if __name__ == '__main__':
    main()