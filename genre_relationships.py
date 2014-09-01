'''
Created on Apr 9, 2014

@author: daniel-allington
'''

# Creates a new database containing: (a) table of genre strings, with
# absolute frequencies, in order of frequency, leaving out any below a
# given threshold of frequency; (b) as a but for tags; (c) table of
# users with tracks, giving (i) all genre strings associated with each
# user's tracks, with frequency, in order of frequency, (ii) the
# user's most common genre string, (iii) the user's most common three
# genre strings (in alphabetical ordre; (d) as c but for tags. This
# database is stored in an sqlite file with '_deriv' appended to the
# name of the database it's derived from.

# Where the program has to choose between genres/tags that a user has
# used with equal frequency, it chooses the one that is more frequent
# in the dataset as a whole (where this is tied, it chooses the
# shorter string; where that is tied, the alphabetically prior
# string).

# Purpose: it will then be possible to create an undirected network of
# users with edges based not on followings etc but on use of similar
# genres/tags - and a network of genres/tags based on which ones are
# associated with tracks uploaded by the same individuals. Hopefully
# clusters in the two networks will give us a sense of the broad
# stylistic groupings behind the huge range of genre terms used on
# SoundCloud. Calculating betweenness centrality for these clusters
# will help to identify key terms and individuals.

# Edit: this now removes all spaces and hyphens from within strings.
# Reason is to stop 'hip hop', 'hip-hop', and 'hiphop' appearing as
# three different things.

import sqlite3
import re
import collections
import add_data
import cPickle
import deriv_db


genre_sep = re.compile(r'"|,|/|\\')
tag_captu = re.compile(r'"(.+?)"|\b(\S+?)\b')
to_remove = re.compile(r'[ -]')

genre_threshold = 2 
tag_threshold = 2

f = open('stopwords') # extracted from NLTK
stop = cPickle.load(f)
f.close()

def flatten(l):
    return [i for subl in l for i in subl]


def user_data(curs,user,col):
    # Apologies for combining a string operation with the proper
    # SQLite insertion method (with ?) - for some reason, when I try
    # to insert a table name with ?, it thinks this is a value that I
    # want it to return. The database is safe so this isn't the
    # security issue that it might have been - but I'll change it once
    # I figure out how.
    return curs.execute('SELECT {} FROM tracks WHERE user_id=?'.format(col),(user,))


def all_genres(curs):
    curs.execute('SELECT * FROM sqlite_master')
    return curs.execute('SELECT genre FROM tracks')


def all_tags(curs):
    return curs.execute('SELECT tag_list FROM tracks')


def clean(l):
    l2=[to_remove.sub('',i) for i in l]
    return [i for i in l2 if len(i)>1 and i not in stop]


def strings_from_string(s,col):
    if col=='genre':
        return clean([g.strip() 
                      for g in genre_sep.split(s.lower().strip('"\' '))])
    elif col=='tag_list':
        return clean([group[0] if group[0] else group[1] 
                      for group in tag_captu.findall(s.lower())])
    else: print 'Unrecognised source column name: {}'.format(col)


def strings_from_iterator(ite,col):
    strings=[]
    for i in ite:
        if i[0]: strings.extend(strings_from_string(i[0],col))
    return strings


def n_from_list(l,n,cursderiv,ranktable):
    sorting_list=[]
    for item in l:
        cursderiv.execute('SELECT rank FROM {} WHERE string=?'.format(ranktable),
                          (item[0],))
        c = cursderiv.fetchone()
        if c: rank=c[0]
        else: rank=10000000
        sorting_list.append((rank,len(item[0]),item[0]))
    return [(i[2],) for i in sorted(sorting_list)[:n]]


def n_most_common(counted,n,cursderiv,ranktable):
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
        l.extend(n_from_list(current,n-len(l),cursderiv,ranktable))
    string_list=[i[0] for i in l]
    return sorted(string_list+(['']*(n-len(string_list))))


def add_ranks(l,threshold):
    if not l: return [('','',0)]
    counted = collections.Counter(l).most_common()
    nums=list(reversed(sorted(set(zip(*counted)[1]))))
    return [(c[0],c[1],nums.index(c[1])+1) for c in counted if c[1]>=threshold]


def create_gt_table(curssourc,cursderiv,colsourc,tabderiv):
    add_data.create_table(cursderiv,tabderiv)
    entries = (all_genres(curssourc) if tabderiv=='genres' 
               else all_tags(curssourc))
    l = []
    for e in entries:
        if e[0]: 
            l.extend(strings_from_string(e[0],colsourc))
    sql=('INSERT INTO {} (string,frequency,rank) '
         'VALUES(?,?,?)'.format(tabderiv))
    thresh = (genre_threshold if tabderiv == 'genres' else tag_threshold)
    cursderiv.executemany(sql,add_ranks(l,thresh))


def check_tables(cursderiv,required_tables):
    tables_present=[]
    for t in required_tables:
        cursderiv.execute("SELECT name FROM sqlite_master WHERE type='table' "
                          "AND name=?",(t,))
        tables_present.append(True if len (cursderiv.fetchall()) > 0 
                              else False)
    return tables_present


def gt_tables(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc = connsourc.cursor()
    cursderiv = connderiv.cursor()
    for colsourc,table in [('genre','genres'),('tag_list','tags')]:
        create_gt_table(curssourc,cursderiv,colsourc,table)
        connderiv.commit()


def deriv_user_data(curssourc,cursderiv,users,colsourc,ranktable):
    for user in users:
        print 'Working with user: '+str(user)
        to_count=strings_from_iterator(user_data(curssourc,user[0],colsourc),
                                       colsourc)
        counted=collections.Counter(to_count).most_common()
        mcstring = unicode(n_most_common(counted,
                                         1,cursderiv,ranktable)[0])
        cstrings = ' | '.join(n_most_common(counted,
                                            3,cursderiv,ranktable))
        str_counted= ' | '.join([u'{}, {}'.format(c[0],c[1]) 
                                 for c in counted])
        yield user[0],str_counted,mcstring,cstrings


def user_gt_tables(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc = connsourc.cursor()
    cursderiv = connderiv.cursor()

    required=['genres','tags']
    ct = check_tables(cursderiv,required)
    if not ct[0] or not ct[1]:
        for n,r in enumerate(ct):
            if not r: print 'Could not find {} table.'.format(required[n])
        print ('Before calling this function, call gt_tables with '
               'path of source database to create necessary tables.')
        return False

    curssourc.execute('SELECT user_id FROM tracks')
    users=set(curssourc.fetchall())

    for colsourc,tabderiv,ranktable in [('genre','user_genres','genres'),
                                        ('tag_list','user_tags','tags')]:
        print 'Now working with: '+ranktable
        add_data.create_table(cursderiv,tabderiv)
        add_data.insert_deriv_data(cursderiv,tabderiv,
                                   deriv_user_data(curssourc,cursderiv,
                                                   users,colsourc,ranktable))
        connderiv.commit()

    return True
