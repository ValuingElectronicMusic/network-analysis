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
    while userfound == False: # SoundCloud has about 55 million users at this time - return random number between 0 and 250 million
        userId = random.randint(0, 250000000)
        print '----trying with user id ' + str(userId) # try to get a track
        try:
            user = client.get('/users/' + str(userId))
        except Exception as e:
            print 'Error: %s' % (e.message)
        else:
            userfound = True    
    return user


def getSnowballSample(numUsers):
    user = getRandomUser()

    return user


def main(): 
     
    sample = getSnowballSample(25)
    print('User found: '+sample.username)