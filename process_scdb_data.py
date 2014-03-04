#!/usr/bin/env python

# This comprises a function to get all the data out of the sqlite
# table where it's been stored, three classes to hold that data in an
# easily accessible form, and a bunch of functions to calculate stuff
# from data stored in instances of those classes. At the end of the
# file, there's a function called 'demonstrate' that shows what a few
# of these do.

import getSoundCloudData as scd
from sqlite3 import connect

db_path = 'scdb.sqlite'

def get_table(tableName):
    '''Returns contents of one entire table from the sqlite database.'''
    conn = connect(db_path)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM {!s}".format(tableName))
        return curs.fetchall()

#class data_holder():
#    'Temp use of the data_holder class to populate the data using methods from getSoundCloud Data rather than from external db.'
#
#    def __init__(self):
#        scd.getNewSnowballSample(15)
#
#        # self.agents = set of SoundCloud user objects
#        self.agents = scd.agents
#        # self.x_follows_y = set of SoundCloud follow relationship tuples (x, y) where SC agent x follows SC agent y
#        self.x_follows_y = scd.x_follows_y
#        # self.tracks = set of SoundCloud track objects where tracks belong to users in self.agents
#        self.tracks = scd.tracks
        
class data_holder():
    'An object to hold data from each of the four tables in the database.'

    def __init__(self):
        self.agents = set(get_table('agents'))
        self.x_follows_y = set(get_table('x_follows_y'))
#        self.authorings = set(get_table('Authorings'))
        self.tracks = set(get_table('tracks'))

class entity_holder():
    'An object to hold data cheaply processed from those held in the above.'

    def __init__(self, data):
        self.agents = {x[0] for x in data.agents}
#        self.users = {x[0] for x in data.agents if len(x[0]) != 10}
#        self.nonusers = {x[0] for x in data.agents if len(x[0]) == 10}
        self.authors = {x[8] for x in data.tracks}
#        self.tracks = {x[0] for x in data.tracks}
#        self.receivers = {x[0] for x in data.x_follows_y}
#        self.received = {x[1] for x in data.x_follows_y}
#        self.rated = {x[1] for x in data.x_follows_y if x[2] >= 1}
#        self.raters = {x[0] for x in data.x_follows_y if x[2] >= 1}
#        self.recognitions = {x[:2] for x in data.x_follows_y # for self.followers 
#                             if x[2] >= rating_threshold}
#        self.highrated = {x[1] for x in self.recognitions}
#        self.followed = {x[0] for x in data.authorings 
#                           if x[1] in self.highrated}
        self.followed = {x[1] for x in data.x_follows_y}
        self.followers = {x[0] for x in data.x_follows_y}
#        self.author_users = self.authors & self.users
#        self.author_receivers = self.authors & self.receivers
#        self.author_raters = self.authors & self.raters
#        self.author_recognisers = self.authors & self.followers
#        self.recognised_recognisers = self.followed & self.followers
#        self.active_users = self.author_users | self.receivers

#class attribute_holder():
#    'An object to hold ranges of categorical values for some variables.'
#
#    def __init__(self,data):
#        self.years = {x[2] for x in data.tracks}
#        self.languages = {x[3] for x in data.tracks}
#        self.dev_systems = {x[4] for x in data.tracks}
#

def printData(data):
    print('data.agents (max 10, selected at random from '+str(len(data.agents))+' agents)')
    temp_copy = data.agents.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent '+str(popped[0])+' '+popped[2])
        count = count+1
    
    print ''
    print('data.x_follows_y relationships (max 10 selected at random from '+str(len(data.x_follows_y))+' follow relationships)')
    temp_copy = data.x_follows_y.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped[0])+' follows '+str(popped[1]))
        count = count+1
        
    print ''
    print('data.tracks (max 10 selected at random from '+str(len(data.tracks))+' tracks)')
    temp_copy = data.tracks.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        try:  # might throw a type error if there are strange characters in the title or genre for a track
            print(str(count)+'. agent id: '+str(popped[8])+', track id: '+str(popped[0])+', title: '+popped[9]+', genre: '+popped[31])
        except Exception as e:
            print(str(count)+'. agent id: '+str(popped[8])+', track id: '+str(popped[0])+', title and genre - error in displaying, '+ e.message)
        count = count+1
#    print('data.agents (max 10, selected at random from '+str(len(data.agents))+' data.agents)')
#    temp_copy = data.agents.copy()
#    count=0;
#    while (count<10 and len(temp_copy)>0):
#        popped = temp_copy.pop()
#        print(str(count)+'. agent '+str(popped.id)+' '+popped.username)
#        count = count+1
#    
#    print ''
#    print('x_follows_y relationships (max 10 selected at random from '+str(len(data.x_follows_y))+' follow relationships data.x_follows_y)')
#    temp_copy = data.x_follows_y.copy()
#    count=0;
#    while (count<10 and len(temp_copy)>0):
#        popped = temp_copy.pop()
#        print(str(count)+'. agent id: '+str(popped[0])+' follows '+str(popped[1]))
#        count = count+1
#        
#    print ''
#    print('data.tracks (max 10 selected at random from '+str(len(data.tracks))+' data.tracks)')
#    temp_copy = data.tracks.copy()
#    count=0;
#    while (count<10 and len(temp_copy)>0):
#        popped = temp_copy.pop()
#        try:  # might throw a type error if there are strange characters in the title or genre for a track
#            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title: '+popped.title+', genre: '+popped.genre)
#        except Exception as e:
#            print(str(count)+'. agent id: '+str(popped.user_id)+', track id: '+str(popped.id)+', title and genre - error in displaying, '+ e.message)
#        count = count+1

def printEntities(entities):
    print ''
    print('entities.agents - max 10 selected at random from total of '+str(len(entities.agents)))
    temp_copy = entities.agents.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped))
        count = count+1
    
    print ''
    print('entities.authors (max 10 selected at random from total of '+str(len(entities.authors)))
    temp_copy = entities.authors.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped))
        count = count+1

    print ''
    print('entities.followers (max 10 selected at random from total of '+str(len(entities.followers)))
    temp_copy = entities.followers.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped))
        count = count+1

    print ''
    print('entities.followed (max 10 selected at random from total of '+str(len(entities.followed)))
    temp_copy = entities.followed.copy()
    count=0;
    while (count<10 and len(temp_copy)>0):
        popped = temp_copy.pop()
        print(str(count)+'. agent id: '+str(popped))
        count = count+1


#def works_by_system(data):
#    '''Returns a dictionary: keys are systems; values, tracks created therewith.
#
#    Note that this doesn't bother with the full range of values in the
#    data. Only the most common systems are returned, and different
#    versions of a system are treated as the same system (e.g. 'Inform
#    6' and 'Inform 7' games are grouped together under 'Inform').'''
#
#    ADRIFT_list = []
#    Inform_list = []
#    TADS_list   = []
#    ZIL_list    = []
#    Quill_list  = []
#    Eamon_list  = []
#    Scott_list  = []
#    Hugo_list   = []
#
#    for work in data.tracks:
#        if not work[4]: continue
#        if 'ADRIFT' in work[4]:
#            ADRIFT_list.append(work[0])
#        elif 'Inform' in work[4]:
#            Inform_list.append(work[0])
#        elif 'TADS' in work[4]:
#            TADS_list.append(work[0])
#        elif 'ZIL' in work[4]:
#            ZIL_list.append(work[0])
#        elif 'Hugo' in work[4]:
#            Hugo_list.append(work[0])
#        elif 'Quill' in work[4]:
#            Quill_list.append(work[0])
#        elif 'Eamon' in work[4]:
#            Eamon_list.append(work[0])
#        elif 'Scott' in work[4]:
#            Scott_list.append(work[0])
#    return {'adrift':set(ADRIFT_list), 'inform':set(Inform_list), 
#            'tads':set(TADS_list), 'zil':set(ZIL_list), 
#            'quill':set(Quill_list), 'eamon':set(Eamon_list),
#            'scott':set(Scott_list), 'hugo':set(Hugo_list)}
#
def name_agent(id,data_agents):
    '''Returns the human-readable name associated with an ID of an agent.'''

    for a in data_agents:
        if (a[0]==id):
            return a[2]

#def year_of(work_ID,data):
#    'Returns the year a particular work was released.'
#
#    return next((work for work in data.tracks if work[0] == work_ID))[2]
#
#def attribute_entity_dict(attribute,entity_set,attr_index):
#    'Returns a dictionary of entities with a particular attribute.'
#
#    return {attr:{member[0] for member in entity_set 
#                  if member[attr_index] == attr}
#            for attr in attribute}
#
#def work_number_and_mean_ratings(work,data):
#    'Returns the number of ratings and the mean rating that a work received.'
#
#    ratings = [r for r in work_ratings(work,data)]
#    num_ratings = len(ratings)
#    if num_ratings == 0: return 0,0
#    else:
#        num_ratings = sum([r[2] for r in ratings])/float(num_ratings)
#        return num_ratings,mean_ratings
#
#def most_rated(data):
#    'Returns list of tuples in order of ranking of tracks by number of ratings.'
#
#    return sorted([work_number_and_mean_ratings(work,data) + (work,)
#                   for work in data.tracks])[::-1]
#
#def authors_of(work,data):
#    'Returns set of agents credited with authorship of a single work.'
#
#    return {authoring[0] for authoring in data.authorings 
#            if authoring[1] == work}
#
#def works_by(author,data):
#    'Returns set of tracks for which an author is credited.'
#
#    return {track[0] for track in data.tracks
#            if track[8] == author}

#def recognisers_of(work,entities,data):
#    '''Returns set of agents who rated a given work highly.
#
#    Note that ratings of tracks for which the rater is credited as an
#    author are excluded.'''
#
#    return {rec[0] for rec in entities.recognitions
#            if rec[1] == work
#            and rec[1] not in works_by(rec[0],data)}

def followers_of_author(author,data):
    '''Returns set of agents who follow a given author'''

    followers = set([])
    for follow in data.x_follows_y:
        if (follow[1]==author):
            followers = followers | follow[0]
    return followers

#def total_receptions_attribute(attribute,attr_entity_dict,data):
#    'Returns all x_follows_y of tracks with the given value for one variable.'
#
#    return {reception for reception in data.x_follows_y
#            if reception[1] in attr_entity_dict[attribute]}
#
#def dict_total_receptions_attribute_type(att_type,att_entity_dict,data):
#    '''Returns a dictionary of x_follows_y of tracks for one variable.
#
#    Key is every value which that variable has in the data. I used
#    this for comparing the number of ratings and reviews received by
#    tracks in different languages, released in different years, or
#    developed with different authoring systems.'''
#
#    return {att:total_receptions_attribute(att,att_entity_dict,data)
#            for att in att_type}
#
#def demonstrate():
#    'This is just to show how things work.'
#
#    data = data_holder()
#    entities = entity_holder(data)
#    attributes = attribute_holder(data)
#
#    sys_works  = attribute_entity_dict(attributes.dev_systems,data.tracks,4)
#    inf6_receps = total_receptions_attribute('Inform 6',sys_works,data)
#    print 'Receptions of Inform 6 tracks: {}\n'.format(len(inf6_receps))
#
#    lang_works = attribute_entity_dict(attributes.languages,data.tracks,3)
#    print 'Works in Russian: {}'.format(len(lang_works['Russian (ru)']))
#
#    lang_receptions = dict_total_receptions_attribute_type(attributes.languages,lang_works,data)
#    print 'Receptions of tracks in Russian: {}\n'.format(len(lang_receptions['Russian (ru)']))
#    # Note that most languages were entered with multiple variants of the same
#    # string. Russian happened not to be, probably because there were just two
#    # tracks.
#
#    year_works = attribute_entity_dict(attributes.years,data.tracks,2)
#    year_receptions = dict_total_receptions_attribute_type(attributes.years,year_works,data)
#    print 'Works and x_follows_y by year'
#    print 'Year\tWorks\tReceptions of those tracks'
#    for y in attributes.years:
#        print '{}\t{}\t{}'.format(y,len(year_works[y]),len(year_receptions[y]))
