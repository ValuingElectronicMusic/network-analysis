'''
Created on Apr 9, 2014

@author: daniel-allington
'''

# (1) Creates a new database containing all genres and tags, with
# absolute frequencies, in order of frequency, leaving out any below a
# given threshold of frequency. (2) For a list of users, identifies
# all the genres and tags associated with each user's tracks, counting
# how frequently each occurs for that user, and also produces a list
# of each user's n most frequently used genres and tags. Where it has
# to choose between genres/tags that a user has used with equal
# frequency, it chooses the one that is more frequent in the dataset
# as a whole (where this is tied, it chooses the shorter string; where
# that is tied, the alphabetically prior string). At the moment, this
# is printed out. Call the test() function to see.

# Remaining to be done: the current printed output should be stored in
# a table of the new sqlite database. The function for creating that
# output should no longer call the function that creates the frequency
# tables of genres and tags in the same database; instead, it should
# throw an error if those tables don't yet exist, prompting the user
# to call the function that creates them. These two functions should
# be called something more informative than 'main'.

# Purpose: it will then be possible to create an undirected network of
# users with edges based not on followings etc but on use of similar
# genres/tags - and a network of genres/tags based on which ones are
# associated with tracks uploaded by the same individuals. Hopefully
# clusters in the two networks will give us a sense of the broad
# stylistic groupings behind the huge range of genre terms used on
# SoundCloud. Calculating betweenness centrality for these clusters
# will help to identify key terms and individuals.

# Note that nltk needs to be installed, with corpus data. This is
# purely for the list of stopwords, which could have been obtained by
# other means! But we'll be needing nltk's core functionality soon
# enough.


import sqlite3
import re
import collections
from nltk.corpus import stopwords


genre_sep = re.compile(r'"|,|/|\\')
tag_captu = re.compile(r'"(.+?)"|\b(\S+?)\b')
stop = stopwords.words('english')

genre_threshold = 2 
tag_threshold = 2


def flatten(l):
    return [i for subl in l for i in subl]


def user_data(curs,user):
    curs.execute('SELECT genre,tag_list FROM tracks WHERE user_id=?',(user,))
    return zip(*curs.fetchall())
    

def all_genres(curs):
    return curs.execute('SELECT genre FROM tracks')


def all_tags(curs):
    return curs.execute('SELECT tag_list FROM tracks')


def clean(l):
    return [i for i in l if len(i)>1 and i not in stop]


def genres_from_string(s):
    return clean([g.strip() for g in genre_sep.split(s.lower().strip('"\' '))])


def tags_from_string(s):
    return clean([group[0] if group[0] else group[1] 
                  for group in tag_captu.findall(s.lower())])


def user_strings(l,func):
    return flatten([func(t) for t in l])


def n_from_list(l,n,cursderiv,table):
    sorting_list=[]
    for item in l:
        cursderiv.execute('SELECT rank FROM genres WHERE string=?',(item[0],))
        c = cursderiv.fetchone()
        if c: rank=c[0]
        else: rank=1000000
        sorting_list.append((rank,len(item[0]),item[0]))
    return [(i[2],) for i in sorted(sorting_list)[:n]]


def n_most_common(counted,n,cursderiv,table):
    c = (x for x in counted)
    l = []
    unused = None
    current= []
    while c:
        while True:
            try:
                item = c.next()
                if not current:
                    current.append(item)
                elif item[1] == current[0][1]:
                    current.append(item)
                else:
                    unused = [item]
                    break
            except StopIteration:
                c=False
                break
        if len(l)+len(current) <= n:
            l.extend(current)
            current = unused            
            unused = None
        else:
            break
    if current:
        l.extend(n_from_list(current,n-len(l),cursderiv,table))
    string_list=[i[0] for i in l]
    return string_list+(['']*(n-len(string_list)))


def count_up(strings,n,curs,table):
    counted=collections.Counter(strings).most_common()
    return counted, n_most_common(counted,n,curs,table)


def add_ranks(l,threshold):
    counted = collections.Counter(l).most_common()
    nums=list(reversed(sorted(set(zip(*counted)[1]))))
    return [(c[0],c[1],nums.index(c[1])+1) for c in counted if c[1]>=threshold]


def create_genres_table(curssourc,cursderiv):
    cursderiv.execute('CREATE TABLE genres(string PRIMARY KEY, '
                      'frequency INTEGER, rank INTEGER)')
    gen_entries = all_genres(curssourc)
    gen_l = []
    for g in gen_entries:
        if g[0]: 
            gen_l.extend(genres_from_string(g[0]))
    sql=('INSERT INTO genres (string,frequency,rank) VALUES(?,?,?)')
    cursderiv.executemany(sql,add_ranks(gen_l,genre_threshold))


def create_tags_table(curssourc,cursderiv):
    cursderiv.execute('CREATE TABLE tags(string PRIMARY KEY, '
                      'frequency INTEGER, rank INTEGER)')
    tag_entries = all_tags(curssourc)
    tag_l = []
    for t in tag_entries:
        if t[0]:
            tag_l.extend(tags_from_string(t[0]))
    sql=('INSERT INTO tags (string,frequency,rank) VALUES(?,?,?)')
    cursderiv.executemany(sql,add_ranks(tag_l,tag_threshold))


def deriv_tables(curssourc,cursderiv):
    cursderiv.execute("SELECT name FROM sqlite_master WHERE type='table' "
                      "AND name='genres'")
    if len (cursderiv.fetchall()) < 1: 
        create_genres_table(curssourc,cursderiv) 
    cursderiv.execute("SELECT name FROM sqlite_master WHERE type='table' "
                      "AND name='tags'")
    if len (cursderiv.fetchall()) < 1: 
        create_tags_table(curssourc,cursderiv)


def main(db_source,users):
    if db_source[-7:]!='.sqlite': db_source=db_source+'.sqlite'
    db_deriv = db_source[:-7]+'_deriv'+db_source[-7:]
    connsourc = sqlite3.connect(db_source)
    curssourc = connsourc.cursor()
    connderiv = sqlite3.connect(db_deriv)
    cursderiv = connderiv.cursor()
    deriv_tables(curssourc,cursderiv)
    connderiv.commit()

    for user in users:
        genres,tags = user_data(curssourc,user)
        cgens = count_up(user_strings(genres,genres_from_string),
                         3,cursderiv,'genres')
        ctags = count_up(user_strings(tags,tags_from_string),
                         3,cursderiv,'tags')
        print ('User: {}'
               '\nMost common genres: {}'
               '\nMost common tags: {}'.format(user,cgens[1],ctags[1]))

def test():
    main('scdb.sqlite',[118312,132240,942279])
