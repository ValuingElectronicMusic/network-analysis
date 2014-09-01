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

# Edit: also had to include a dictionary of synonyms for the most
# common cases (r&b/rnb, d&b/dnb/drumandbass/drum&bass)

import re
import collections
import add_data
import cPickle
import deriv_db


genre_sep = re.compile(r'"|,|/|\\')
tag_captu = re.compile(r'"(.+?)"|\b(\S+?)\b')
to_remove = re.compile(r'[ -]')

synonyms = {'rnb':'r&b',
            'dnb':'d&b','drumandbass':'d&b','drum&bass':'d&b',
            'housemusic':'house'}

genre_threshold = 2 
tag_threshold = 2

user_batch = 1000

f = open('stopwords') # extracted from NLTK
stop = cPickle.load(f)
f.close()

def flatten(l):
    return [i for subl in l for i in subl]


def all_genres(curs):
    return curs.execute('SELECT user_id, genre FROM tracks')


def all_tags(curs):
    return curs.execute('SELECT user_id, tag_list FROM tracks')


def clean(l):
    l2=[to_remove.sub('',i) for i in l]
    l2=[synonyms[i] if i in synonyms else i for i in l2]
    return [i for i in l2 if len(i)>1 and i not in stop]


def strings_from_string(s,col):
    if not s: return []
    if col=='genre':
        return clean([g.strip() 
                      for g in genre_sep.split(s.lower().strip('"\' '))])
    elif col=='tag_list':
        return clean([group[0] if group[0] else group[1] 
                      for group in tag_captu.findall(s.lower())])
    else: print 'Unrecognised source column name: {}'.format(col)


def split_gt_string(gt_string):
    return [s.strip() for s in gt_string.split('|')]


def process_track_datum(datum):
    return (datum[0:5]+(' | '.join(strings_from_string(datum[5],'tag_list')),)+
            datum[6:8]+(' | '.join(strings_from_string(datum[8],'genre')),)+
            datum[9:])


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
    l=[i for i in l if i]
    if not l: return [('','',0)]
    counted = collections.Counter(l).most_common()
    nums=list(reversed(sorted(set(zip(*counted)[1]))))
    return [(c[0],c[1],nums.index(c[1])+1) for c in counted if c[1]>=threshold]


def copy_sample_table(curssourc,cursderiv):
    add_data.create_table(cursderiv,'sample')
    sql1='SELECT id FROM sample'
    sql2='INSERT INTO sample VALUES(?)'
    cursderiv.executemany(sql2,curssourc.execute(sql1))


def create_uploaders_table(cursderiv):
    add_data.create_table(cursderiv,'uploaders')
    sql1='SELECT user_id FROM tracks'
    sql2='INSERT INTO uploaders VALUES(?)'
    cursderiv.execute(sql1)
    ups=set(cursderiv.fetchall())
    cursderiv.executemany(sql2,ups)
    

def create_sample_uploaders_table(cursderiv):
    add_data.create_table(cursderiv,'sample_uploaders')
    sql1='SELECT id FROM sample'
    sql2='SELECT id FROM uploaders'
    sql3='INSERT INTO sample_uploaders VALUES(?)'
    cursderiv.execute(sql1)
    smp=set(cursderiv.fetchall())
    cursderiv.execute(sql2)
    smp_upl=smp & set(cursderiv.fetchall())
    cursderiv.executemany(sql3,smp_upl)


def copy_and_process_tracks_table(curssourc,cursderiv):
    add_data.create_table(cursderiv,'tracks')
    sql1='SELECT * FROM tracks'
    sql2='INSERT INTO tracks VALUES({})'.format(('?,'*40)[:-1])
    cursderiv.executemany(sql2,
                          (process_track_datum(t) 
                           for t in curssourc.execute(sql1)))


def create_gt_table(cursderiv,colsourc,tabderiv,users):
    add_data.create_table(cursderiv,tabderiv)
    entries = (all_genres(cursderiv) if tabderiv=='genres' 
               else all_tags(cursderiv))
    l = []
    for e in entries:
        if users and e[0] not in users: pass
        elif e[1]:
            l.extend(split_gt_string(e[1]))
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


def copy_tables_across(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc = connsourc.cursor()
    cursderiv = connderiv.cursor()
    copy_sample_table(curssourc,cursderiv)
    copy_and_process_tracks_table(curssourc,cursderiv)
    create_uploaders_table(cursderiv)
    create_sample_uploaders_table(cursderiv)
    connderiv.commit()


def gt_tables(db_source,sample_only=False):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc = connsourc.cursor()
    cursderiv = connderiv.cursor()
    if sample_only:
        cursderiv.execute('SELECT id FROM sample')
        users=set(curssourc.fetchall())
    else: users=None
    for colsourc,table in [('genre','genres'),('tag_list','tags')]:
        create_gt_table(cursderiv,colsourc,table,users)
        connderiv.commit()


def deriv_user_data(all_tracks,cursderiv,users,colsourc,ranktable):
    for user in users:
        try:
            to_count=all_tracks[user[0]]
            counted=collections.Counter(to_count).most_common()
            mcstring = unicode(n_most_common(counted,
                                             1,cursderiv,ranktable)[0])
            cstrings = ' | '.join(n_most_common(counted,
                                                3,cursderiv,ranktable))
            str_counted= ' | '.join([u'{}, {}'.format(c[0],c[1]) 
                                     for c in counted])
            yield user[0],str_counted,mcstring,cstrings
        except KeyError:
            yield user[0],None,None,' | | '


def user_gt_tables(db_source, sample_only=False,tags_too=False):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc = connsourc.cursor()
    cursderiv = connderiv.cursor()

    required=['sample','tracks','uploaders','genres','tags']
    if False in check_tables(cursderiv,required):
        return False
   
    if sample_only: 
        cursderiv.execute('SELECT id FROM sample')
        users=cursderiv.fetchall()
        cursderiv.execute('SELECT id FROM uploaders')
        users=list(set(users).intersection(set(cursderiv.fetchall())))
    else: 
        cursderiv.execute('SELECT id FROM uploaders')
        users=cursderiv.fetchall()

    print '{} users to process'.format(len(users))

    to_do = [('genre','user_genres','genres')]
    if tags_too: to_do.append(('tag_list','user_tags','tags'))

    for colsourc,tabderiv,ranktable in to_do:
        print 'Now working with: '+ranktable
        add_data.create_table(cursderiv,tabderiv)
        print 'Fresh {} table created.'.format(colsourc)
        print 'Getting track data.'
        tracks={}
        sql='SELECT user_id,{} FROM tracks'.format(colsourc)
        for t in cursderiv.execute(sql):
            l=split_gt_string(t[1])
            if l[0]:
                try:
                    tracks[t[0]].extend(l)
                except KeyError:
                    tracks[t[0]]=l
        print 'Data loaded in memory.'
        done=0
        while done < len(users):
            to_collect = (user_batch if done+user_batch <= len(users)
                          else len(users)-done)
            this_batch=users[done:done+to_collect]
            print 'Starting on a batch of {} users.'.format(to_collect)
            add_data.insert_deriv_data(cursderiv,tabderiv,
                                       deriv_user_data(tracks,
                                                       cursderiv,this_batch,
                                                       colsourc,ranktable))
            connderiv.commit()
            done+=to_collect
            print '{} done. {} remain.'.format(done,len(users)-done)

    return True


def user_frequency_tables(db_source, sample=True, tags_too=False):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    cursderiv = connderiv.cursor()

    required=['user_genres','user_tags']
    ct = check_tables(cursderiv,required)
    if not ct[0] or not ct[1]:
        for n,r in enumerate(ct):
            if not r: print 'Could not find {} table.'.format(required[n])
        print ('Before calling this function, call user_gt_tables with '
               'path of source database to create necessary tables.')
        return False

    if sample:
        cursderiv.execute('SELECT id FROM sample')
        sample={c[0] for c in cursderiv.fetchall()}

    to_do = [('user_genres','genre_popularity')]
    if tags_too: to_do.append(('user_tags','tag_popularity'))

    for usertab,poptab in to_do:
        cursderiv.execute('SELECT user,most_used FROM {}'.format(usertab))
        if sample:
            strings=[s[1] for s in cursderiv.fetchall() if s[0] in sample]
        else:
            strings=[s[1] for s in cursderiv.fetchall()]

        add_data.create_table(cursderiv,poptab)
        sql=('INSERT INTO {} (string,frequency,rank) '
             'VALUES(?,?,?)'.format(poptab))
        cursderiv.executemany(sql,add_ranks(strings,1))
        connderiv.commit()
