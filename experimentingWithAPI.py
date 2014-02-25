'''
Created on 21 Feb 2014

@author: annaj
'''
import random
import soundcloud   # @UnresolvedImport
import ifdb_sna as isna
import process_ifdb_data as pifdata


def get6emtracks(client):
    random_offset = random.randint(0, 8000)
    print('get 6 electronic music tracks starting from track '+str(random_offset))
    em_tracks = client.get('/tracks', genres='electronic', limit=6, offset=random_offset)
    count = 0
    for emtrack in em_tracks:
        count += 1
        print(str(count) + ' ' + emtrack.title + ' ' + emtrack.permalink_url)
    return em_tracks[0]


def getAllFollowers(client):
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
        

def experimentWithTracks(client):
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
    
    
def getAllTrackComments(client, track):
    comments = client.get('/tracks/%d/comments' % track.id, limit=10)
    for comment in comments:
        print(comment.body+' @'+comment.user["username"])
    
        
def getAllUserComments(client, user):
    comments = client.get('/users/'+str(user.id)+'/comments', limit=10)
    for comment in comments:
        print comment.body
    
    
def main(): 

    import clientSettings as client
    
    client = soundcloud.Client(client_id=client.get_client_id())

    #print 'Demonstrating process_ifdb_data'
    #pifdata.demonstrate()
    
    #print 'Demonstrating ifdb_sna'
    #demo = isna.demonstrate()

    experimentWithTracks(client)
    
    track = get6emtracks(client)
    
    print '** get 10 followers/10 followings of a user'
    user = getAllFollowers(client)
    
    print '** get 10 comments on an electronic track'
    getAllTrackComments(client, track)
    
    print '** get 10 comments made by a given user'
    getAllUserComments(client, user)
       
    
    
