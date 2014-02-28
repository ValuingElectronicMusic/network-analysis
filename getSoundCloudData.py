'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud
#Set up soundcloud API
import clientSettings as client
client = soundcloud.Client(client_id=client.get_client_id())

# agents = set of SoundCloud user objects
agents = set()
# x_follows_y = set of tuples (x, y) representing follow relationships in SoundCloud where x follows y (and x and y are both in "agents")
x_follows_y = set()
# tracks = set of SoundCloud track objects where tracks belong to users in "agents"
tracks = set()



def printData():
    global agents
    print('agents (max 10, selected at random from '+str(len(agents))+' agents)')
    temp_copy = agents.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent '+str(popped.id)+' '+popped.username)
        count = count+1
    
    global x_follows_y
    print ''
    print('X-follows-Y relationships (max 10 selected at random from '+str(len(x_follows_y))+' follow relationships)')
    temp_copy = x_follows_y.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1
        
    global tracks
    print ''
    print('tracks (max 10 selected at random from '+str(len(tracks))+' tracks)')
    temp_copy = tracks.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        try:  # might throw a type error if there are strange characters in the title or genre for a track
            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title: '+popped.title+', genre: '+popped.genre)
        except Exception as e:
            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title and genre - error in displaying, '+ e.message)
        count = count+1
            
        
def getRandomUser():
    userfound = False
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 200 million
        userId = random.randint(0, 200000000)
        try:
            user = client.get('/users/' + str(userId))
        except Exception as e:
            pass
        else:
            userfound = True    
    return user


def getXUserIDs(limit=10):
    users = set()
    for i in range(0,limit):
        #print i
        users.add(getRandomUser().id)
    return users


def getAllFollowers(user):
    strUserID = str(user.id)
    followers = client.get('/users/'+strUserID+'/followers')
    print('Exploring followers of User = '+ strUserID+' with '+str(len(followers))+' followers')
    return followers


def getAllFollowings(user):
    strUserID = str(user.id)
    followings = client.get('/users/'+strUserID+'/followings')
    print('Exploring following activities of User = '+ strUserID+' who follows '+str(len(followings))+' users')
    return followings


def getNewSnowballSample(sampleSize=10):
    ''' Generates a new sample of users (set to the specified sample size, default 10), also generating 
    data on those users' tracks and follow relationships between the users in the set 
    N.B. This wipes any previously collected samples that are only stored in local memory '''
    
    global agents
    global tracks
    global x_follows_y
    agents = set() # initialised to empty
    x_follows_y = set() # initialised to empty
    tracks = set() # initialised to empty
    
    print('Generating snowball sample with a sample size of '+str(sampleSize))
    while (len(agents)<sampleSize):
        user = getRandomUser() # get a new starting point at random        
        agents.add(user)
        print('Seed user = '+str(user.id))
        if (len(agents)<sampleSize):  #in case adding the new user to our sample brings us to our desired samplesize
            collectUsersFromSeedUser(user,sampleSize)
    
    tracks = getTracks() # populate the contents of the global "tracks" set  with tracks relating to the new sample of users
    

def collectUsersFromSeedUser(user,sampleSize):
    ''' Populate the agents and x_follows_y sets with data sampled from SoundCloud '''
    global agents
    global x_follows_y
    # look for all followers of user    
    followers = getAllFollowers(user)
    # add each follower to agents set
    count=0
    while (len(agents)<sampleSize and count<len(followers)): # repeat till sample size reached
        print('length = '+str(len(agents))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followers = '+str(len(followers)))
        print('user '+str(followers[count].id)+' follows '+str(user.id))
        # Add the follower to the set of SC agents
        agents.add(followers[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
        # Add follows relationships between the follower and this seed user
        x_follows_y.add((followers[count].id, user.id))
        count = count+1
      
    # look for all followings of user    
    followings = getAllFollowings(user)
    # add each follower to agents set
    count=0
    while (len(agents)<sampleSize and count<len(followings)): # repeat till sample size reached
        print('length = '+str(len(agents))+', sampleSize = '+str(sampleSize)+', count = '+str(count)+', len followings = '+str(len(followings)))
        print('user '+str(user.id)+' follows '+str(followings[count].id))
        # Add the follower to the set of SC agents
        agents.add(followings[count]) # NB add() won't duplicate a member of a set - if they are already in the set, they are not added again
        # Add follows relationships between the seed user and the user they follow
        x_follows_y.add((user.id, followings[count].id))
        count = count+1
       
    # repeat this step with each follower as the seed user, picking up the results in agents
    count = 0
    while (len(agents)<sampleSize and count<len(followers)):
        collectUsersFromSeedUser(followers[count],sampleSize)
        count = count+1
        
    # repeat this step with each following (user that the seed user follows) as the seed user, picking up the results in agents
    count = 0
    while (len(agents)<sampleSize and count<len(followings)):
        collectUsersFromSeedUser(followings[count],sampleSize)
        count = count+1
    

def getTracks():
    global agents
    new_tracks = set()
    for agent in agents:
        a_id = agent.id 
        agent_tracks = client.get('/users/'+str(a_id)+'/tracks')
        for a_track in agent_tracks:
            new_tracks.add(a_track)
    return new_tracks

def main(): 
    getNewSnowballSample(15)
    printData() 
