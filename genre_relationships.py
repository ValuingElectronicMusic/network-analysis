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
