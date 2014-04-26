'''
Created on 21 Feb 2014

@author: annaj
'''
import random
import soundcloud
import scdb_sna as scna


def get_6_em_tracks(client):
    random_offset = random.randint(0, 8000)
    print('get 6 electronic music tracks starting from track '+str(random_offset))
    em_tracks = client.get('/tracks', genres='electronic', limit=6, offset=random_offset)
    count = 0
    for emtrack in em_tracks:
        count += 1
        print(str(count) + ' ' + emtrack.title + ' ' + emtrack.permalink_url)
    return em_tracks[0]


def get_all_followers(client):
    print 'resolve user calumbowen'
    user = client.get('/resolve', url='https://soundcloud.com/calumbowen')
    str_user_id = str(user.id)
    print('User = '+ str_user_id)
    print('User has these followers')
    
    print('/users/'+str_user_id+'/followers')
    followers = client.get('/users/'+str_user_id+'/followers', limit=10)
    for follower in followers:
        print(str(follower.id)+' '+follower.username)

    print('User is following these users')
    followings = client.get('/users/'+str_user_id+'/followings', limit=10)
    for following in followings:
        print(str(following.id)+' '+following.username)
    
    print 'User is in these groups'
    groups = client.get('/users/'+str_user_id+'/groups', limit=10)
    for group in groups:
        print(str(group.id)+' '+group.name)
    return user    
        

def experiment_with_tracks(client):
    tracks = client.get('/tracks', limit=10)
    print 'Ten tracks'
    for track in tracks: 
        print track.title
        
    track = client.get('/tracks/30709985')
    print 'title of the specific track'
    print track.title
    print 'resolve track calumbowen/winnose-the-calm-before-the and print id'
    client.get('/resolve', url='https://soundcloud.com/calumbowen/winnose-the-calm-before-the')
    print track.id
    
    
def get_all_track_comments(client, track):
    comments = client.get('/tracks/%d/comments' % track.id, limit=10)
    for comment in comments:
        print(comment.body+' @'+comment.user["username"])
    
        
def get_all_user_comments(client, user):
    comments = client.get('/users/'+str(user.id)+'/comments', limit=10)
    for comment in comments:
        print comment.body
    
    
def main(): 

    import client_settings as client_s
    
    client = soundcloud.Client(client_id=client_s.get_client_id())

    print 'Demonstrating scdb_sna'
    scna.demonstrate()

    experiment_with_tracks(client)
    
    track = get_6_em_tracks(client)
    
    print '** get 10 followers/10 followings of a user'
    user = get_all_followers(client)
    
    print '** get 10 comments on an electronic track'
    get_all_track_comments(client, track)
    
    print '** get 10 comments made by a given user'
    get_all_user_comments(client, user)
       
    
    
