'''
Created on Feb 25, 2014

@author: annajordanous
'''

import random
import soundcloud
#Set up soundcloud API
import clientSettings as client
client = soundcloud.Client(client_id=client.get_client_id())


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

def getSnowballSample(sampleSize):
    print('Generating snowball sample with a sample size of '+str(sampleSize))
    agents = set()
    while (len(agents)<sampleSize):
        user = getRandomUser() # get a new starting point at random        
        agents.add(user)
        print('Seed user = '+str(user.id))
        if (len(agents)<sampleSize):  #in case adding the new user to our sample brings us to our desired samplesize
            agents = collectUsersFromSeedUser(user,agents,sampleSize)
    return agents


def collectUsersFromSeedUser(user,agents,sampleSize):
    # look for all followers of user
    followers = getAllFollowers(user)
    # add each follower to agents set
    count=0
    #print('Len agents= '+str(len(agents))+', len(followers) = '+str(len(followers))+', sampleSize= '+str(sampleSize))
    while (len(agents)<sampleSize and count<len(followers)):
        #print('While 1 Len agents= '+str(len(agents))+', len(followers) = '+str(len(followers))+', sampleSize= '+str(sampleSize))
        if (not(followers[count] in agents)):
            agents.add(followers[count])
        count = count+1
       
    # repeat this step with each follower as the seed user, picking up the results in agents
    count = 0
    while (len(agents)<sampleSize and count<len(followers)):
        #print('While 2 Len agents= '+str(len(agents))+', len(followers) = '+str(len(followers))+', sampleSize= '+str(sampleSize))
        agents = collectUsersFromSeedUser(followers[count],agents,sampleSize)
        count = count+1
    return agents


def getTracks(agents):
    tracks = set()
    for agent in agents:
        a_id = agent.id 
        agent_tracks = client.get('/users/'+str(a_id)+'/tracks')
        for a_track in agent_tracks:
            #newTrackTuple = (a_id, a_track)
            tracks.add(a_track)
    return tracks

def main(): 
     
    import process_scdb_data as pscd
    data = pscd.data_holder()
    pscd.printData(data) 
    entities = pscd.entity_holder(data)
    pscd.printEntities(entities)