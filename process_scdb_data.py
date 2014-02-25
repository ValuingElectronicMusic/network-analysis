#!/usr/bin/env python

# This comprises a function to get all the data out of the sqlite
# table where it's been stored, three classes to hold that data in an
# easily accessible form, and a bunch of functions to calculate stuff
# from data stored in instances of those classes. At the end of the
# file, there's a function called 'demonstrate' that shows what a few
# of these do.

from sqlite3 import connect

db_path = 'ifdb_data.sqlite'

def get_table(tableName):
    '''Returns contents of one entire table from the sqlite database.'''
    conn = connect(db_path)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM {!s}".format(tableName))
        return curs.fetchall()

class data_holder():
    'An object to hold data from each of the four tables in the database.'

    def __init__(self):
        self.receptions = set(get_table('Receptions'))
        self.producings = set(get_table('Authorings'))
        self.works = set(get_table('Works'))
        self.agents = set(get_table('Agents'))

class entity_holder():
    'An object to hold data cheaply processed from those held in the above.'

    def __init__(self,data,rating_threshold=4):
        self.agents = {x[0] for x in data.agents}
        self.users = {x[0] for x in data.agents if len(x[0]) != 10}
        self.nonusers = {x[0] for x in data.agents if len(x[0]) == 10}
        self.users = {x[0] for x in data.producings}
        self.works = {x[0] for x in data.works}
        self.receivers = {x[0] for x in data.receptions}
        self.received = {x[1] for x in data.receptions}
        self.rated = {x[1] for x in data.receptions if x[2] >= 1}
        self.raters = {x[0] for x in data.receptions if x[2] >= 1}
        self.follow_recognitions = {x[:2] for x in data.receptions 
                             if x[2] >= rating_threshold}
        self.highrated = {x[1] for x in self.follow_recognitions}
        self.recognised = {x[0] for x in data.producings 
                           if x[1] in self.highrated}
        self.followers = {x[0] for x in self.follow_recognitions}
        self.user_users = self.users & self.users
        self.user_receivers = self.users & self.receivers
        self.user_raters = self.users & self.raters
        self.user_followers = self.users & self.followers
        self.recognised_followers = self.recognised & self.followers
        self.active_users = self.user_users | self.receivers

class attribute_holder():
    'An object to hold ranges of categorical values for some variables.'

    def __init__(self,data):
        self.years = {x[2] for x in data.works}
        self.languages = {x[3] for x in data.works}
        self.dev_systems = {x[4] for x in data.works}

def works_by_system(data):
    '''Returns a dictionary: keys are systems; values, works created therewith.

    Note that this doesn't bother with the full range of values in the
    data. Only the most common systems are returned, and different
    versions of a system are treated as the same system (e.g. 'Inform
    6' and 'Inform 7' games are grouped together under 'Inform').'''

    ADRIFT_list = []
    Inform_list = []
    TADS_list   = []
    ZIL_list    = []
    Quill_list  = []
    Eamon_list  = []
    Scott_list  = []
    Hugo_list   = []

    for work in data.works:
        if not work[4]: continue
        if 'ADRIFT' in work[4]:
            ADRIFT_list.append(work[0])
        elif 'Inform' in work[4]:
            Inform_list.append(work[0])
        elif 'TADS' in work[4]:
            TADS_list.append(work[0])
        elif 'ZIL' in work[4]:
            ZIL_list.append(work[0])
        elif 'Hugo' in work[4]:
            Hugo_list.append(work[0])
        elif 'Quill' in work[4]:
            Quill_list.append(work[0])
        elif 'Eamon' in work[4]:
            Eamon_list.append(work[0])
        elif 'Scott' in work[4]:
            Scott_list.append(work[0])
    return {'adrift':set(ADRIFT_list), 'inform':set(Inform_list), 
            'tads':set(TADS_list), 'zil':set(ZIL_list), 
            'quill':set(Quill_list), 'eamon':set(Eamon_list),
            'scott':set(Scott_list), 'hugo':set(Hugo_list)}

def name_entity(id,entity_data):
    '''Returns the human-readable name associated with an ID string.

    To get agent names, pass in the agents variable of a data_holder
    object; to get work names, pass in the works variable of a
    data_holder object.'''

    return next((a[1] for a in entity_data if a[0] == id))

def year_of(work_ID,data):
    'Returns the year a particular work was released.'

    return next((work for work in data.works if work[0] == work_ID))[2]

def attribute_entity_dict(attribute,entity_set,attr_index):
    'Returns a dictionary of entities with a particular attribute.'

    return {attr:{member[0] for member in entity_set 
                  if member[attr_index] == attr}
            for attr in attribute}

def work_number_and_mean_ratings(work,data):
    'Returns the number of ratings and the mean rating that a work received.'

    ratings = [r for r in work_ratings(work,data)] # @UndefinedVariable
    num_ratings = len(ratings)
    if num_ratings == 0: return 0,0
    else:
        num_ratings = sum([r[2] for r in ratings])/float(num_ratings)
        return num_ratings,mean_ratings  # @UndefinedVariable

def most_rated(data):
    'Returns list of tuples in order of ranking of works by number of ratings.'

    return sorted([work_number_and_mean_ratings(work,data) + (work,)
                   for work in data.works])[::-1]

def authors_of(work,data):
    'Returns set of agents credited with authorship of a single work.'

    return {producing[0] for producing in data.producings 
            if producing[1] == work}

def works_by(user,data):
    'Returns set of works for which a user is credited.'

    return {producing[1] for producing in data.producings
            if producing[0] == user}

def followers_of(work,entities,data):
    '''Returns set of agents who rated a given work highly.

    Note that ratings of works for which the rater is credited as a
    user are excluded.
    NB this method will need to be rewritten for SoundCloud data'''

    return {rec[0] for rec in entities.follow_recognitions
            if rec[1] == work
            and rec[1] not in works_by(rec[0],data)}

def followers_of_user(user,entities,data):
    '''Returns set of agents who rated a given user's works highly.

    Note that an agent's ratings of works that he or she co-authored
    with the user in question are excluded.
    NB this method will need to be rewritten for SoundCloud data'''

    followers = set([])
    for work in works_by(user,data):
        followers = followers | followers_of(work,entities,data)
    return followers

def total_receptions_attribute(attribute,attr_entity_dict,data):
    'Returns all receptions of works with the given value for one variable.'

    return {reception for reception in data.receptions
            if reception[1] in attr_entity_dict[attribute]}

def dict_total_receptions_attribute_type(att_type,att_entity_dict,data):
    '''Returns a dictionary of receptions of works for one variable.

    Key is every value which that variable has in the data. I used
    this for comparing the number of ratings and reviews received by
    works in different languages, released in different years, or
    developed with different authoring systems.
    NB authoring systems - out of date comment - different genres?'''

    return {att:total_receptions_attribute(att,att_entity_dict,data)
            for att in att_type}

def demonstrate():
    'This is just to show how things work.'

    data = data_holder()
    entities = entity_holder(data)
    attributes = attribute_holder(data)

    sys_works  = attribute_entity_dict(attributes.dev_systems,data.works,4)
    inf6_receps = total_receptions_attribute('Inform 6',sys_works,data)
    print 'Receptions of Inform 6 works: {}\n'.format(len(inf6_receps))

    lang_works = attribute_entity_dict(attributes.languages,data.works,3)
    print 'Works in Dutch: {}'.format(len(lang_works['Dutch (nl)']))

    lang_receptions = dict_total_receptions_attribute_type(attributes.languages,lang_works,data)
    print 'Receptions of works in Dutch: {}\n'.format(len(lang_receptions['Dutch (nl)']))
    # Note that most languages were entered with multiple variants of the same
    # string. Russian happened not to be, probably because there were just two
    # works.

    year_works = attribute_entity_dict(attributes.years,data.works,2)
    year_receptions = dict_total_receptions_attribute_type(attributes.years,year_works,data)
    print 'Works and receptions by year'
    print 'Year\tWorks\tReceptions of those works'
    for y in attributes.years:
        print '{}\t{}\t{}'.format(y,len(year_works[y]),len(year_receptions[y]))
