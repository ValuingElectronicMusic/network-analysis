# Requires 'sample' table to have been copied into the _deriv.sqlite
# database - it's just easier that way than having two db connections;
# then the original database can be left well alone. Also requires
# the 'tracks' table to have been copied across with the 'tag_list' and 
# 'genre' columns processed. So run copy_tables_across() from
# genre_relationships_sample.py on the original database before running
# any of these functions.

import collections
import sqlite3
import os
import os.path
import csv
import time

the_genres=[('urban',['hiphop','rap','instrumental','trap','r&b','reggae',
                      'beat']),
            ('edm',['house','electronic','dubstep','techno','electro',
                    'd&b','techhouse','progressivehouse','dance','deephouse',
                    'trance','electrohouse','hardstyle','edm','mashup',
                    'ambient']),
            ('other',['pop','rock','acoustic','blues','music','cover','folk',
                      'jazz','piano','classical','indie','alternative','metal',
                      'soundtrack','punk','alternativerock','country','funk',
                      'singersongwriter'])]

def genres_od():
    l=[]
    for t in the_genres:
        for g in t[1]:
            l.append((g,set([])))
    return collections.OrderedDict(l)


def genre_community_od(d):
    l=[]
    for t in the_genres:
        l.append((t[0],set([])))
    od = collections.OrderedDict(l)
    for t in the_genres:
        for g in t[1]:
            od[t[0]].update(d[g])
    return od


def comments_by_genre(curs,target_genre,user_sample=False,English=True):
    if English:
        sql=('SELECT id,commenter,track_creator,track_genre '
             'FROM comments_corp WHERE track_genre IS NOT NULL AND language=1')
    else:
        sql=('SELECT id,commenter,track_creator,track_genre '
             'FROM comments_corp WHERE track_genre IS NOT NULL')
    if user_sample:
        return {c[0] for c in curs.execute(sql) 
                if c[1] in user_sample
                and c[1] != c[2]
                and target_genre in {s.strip() for s in c[3].split('|')}}
    else:
        return {c[0] for c in curs.execute(sql)
                if c[1] != c[2]
                and target_genre in {s.strip() for s in c[3].split('|')}}


def users_by_genre(curs,target_genre,user_sample=False):
    sql=('SELECT user,most_used FROM user_genres WHERE most_used '
         'IS NOT NULL')
    if user_sample:
        return {u[0] for u in curs.execute(sql) if u[0] in user_sample
                and u[1]==target_genre}
    else:
        return {u[0] for u in curs.execute(sql) if u[1]==target_genre}


def tracks_by_genre(curs,target_genre,user_sample=False):
    sql=('SELECT id,user_id,genre FROM tracks WHERE genre IS NOT NULL')
    if user_sample:
        return {t[1] for t in curs.execute(sql) if t[1] in user_sample
                and target_genre in {s.strip() for s in t[2].split('|')}}
    else:
        return {t[1] for t in curs.execute(sql) 
                if target_genre in {s.strip() for s in t[2].split('|')}}
               

def filled_genre_dict(func,curs,user_sample=False,English=False):
    dict=genres_od()
    for genre in dict.keys():
        if English:
            dict[genre].update(func(curs,genre,user_sample,English))
        else:
            dict[genre].update(func(curs,genre,user_sample))
    return dict


def the_sample(curs):
    sql=('SELECT id FROM sample')
    return {s[0] for s in curs.execute(sql)}


def uploaders(curs):
    sql=('SELECT user_id FROM tracks')
    return {t[0] for t in curs.execute(sql)}


def sample_uploaders(curs):
    return the_sample(curs) & uploaders(curs)


def join_comments(corpus):
    return '\n\n'.join([c[1] for c in corpus])


class SpamFilter(object):
    def __init__(self):
        self.comments_seen=set([])
    
    def check_comment(self,comment):
        if comment not in self.comments_seen:
            self.comments_seen.add(comment)
            return True
        else:
            if '%%' in comment:
                return False
            elif len(comment.split()) > 2:
                return False
            else:
                return True


def encode(t):
    return t.encode('utf-8')


def save_corpus(corpus,path='',name='corpus',single_file=True):
    filter = SpamFilter()
    if single_file:
        with open(os.path.join(path,name+'.txt'),'w') as f:
            for comment in corpus:
                if filter.check_comment(comment[1]):
                    f.write(encode(comment[1])+'\n\n')
    else:
        os.mkdir(name)
        for comment in corpus:
            if filter.check_comment(comment[1]):
                with open(os.path.join(path,name,
                                       '{}.txt'.format(comment[0]))
                          ,'w') as f:
                    f.write(encode(comment[1]))
    return filter


def get_comments(curs,comment_set):
    sql=('SELECT id,filtered_text FROM comments_corp ')
    return ((c[0],c[1]) for c in curs.execute(sql) if c[0] in comment_set)


def output_stats(dict,path,name):
    stats=[(g,len(dict[g])) for g in dict.keys()]
    with open(os.path.join(path,name+'.csv'),'wb') as f:
        writer=csv.writer(f,dialect='excel')
        writer.writerows(stats)


def output_corpora(curs,dict,path,single_file=True):
    for g in dict.keys():
        comments = get_comments(curs,dict[g])
        save_corpus(comments,path,g+'_corpus',single_file)


def output_follow_stats(dict,path):
    all_results=open(os.path.join(path,'all_follows_by_genre.csv'),'wb')
    all_res_w=csv.writer(all_results,dialect='excel')
    for gen_com in the_genres:
        com_results=open(os.path.join(path,'follows_by_genre_in_'+gen_com[0]+
                                      '_community.csv'),'wb')
        com_res_w=csv.writer(com_results,dialect='excel')
        for genre in gen_com[1]:
            gen_results=open(os.path.join(path,'follows_by_genre_in_'+genre+
                                          '_genre.csv'),'wb')
            gen_res_w=csv.writer(gen_results,dialect='excel')
            all_res_w.writerows(dict[genre])
            com_res_w.writerows(dict[genre])
            gen_res_w.writerows(dict[genre])
            gen_results.close()
        com_results.close()
    all_results.close()


def percentages(a):
    b=[]
    for i in a[1:]:
        if i:
            b.append(int(i / float(a[0]) * 100 + 0.5))
        else:
            b.append(0)
    return b


def following_within_genre(curssourc,cursderiv,gen_dict):
    everyone_genre=filled_genre_dict(users_by_genre,cursderiv)
    everyone_gen_com=genre_community_od(everyone_genre)
    everyone=set([])
    results_by_gen=collections.OrderedDict()
    for v in everyone_gen_com.values():
        everyone.update(v)
    for genre in gen_dict.keys():
        community=[c[0] for c in the_genres if genre in c[1]][0]
        results=[]
        for user in gen_dict[genre]:
            sql='SELECT followed FROM x_follows_y WHERE follower=?'
            total={f[0] for f in curssourc.execute(sql,(user,))}
            with_genres=total & everyone
            this_com=with_genres & everyone_gen_com[community]
            this_gen=this_com & everyone_genre[genre]
            figures=[len(total),len(with_genres),len(this_com),len(this_gen)]
            results.append(figures+percentages(figures[1:]))
        results_by_gen[genre]=results
    return results_by_gen


def do_everything(db_source,single_file_corpora=True):
    connsourc=sqlite3.connect(db_source)
    curssourc=connsourc.cursor()
    db=db_source[:-7]+'_deriv.sqlite'
    conn=sqlite3.connect(db)
    curs=conn.cursor()
    db_path=os.path.split(db)

    print 'Putting necessary directories in place...'

    base_path=os.path.join(db_path[0],
                           'from_{}_{}'.format(db_path[1],
                                             time.strftime('%Y%m%d_%H%M')))
    stat_path=os.path.join(base_path,'statistics')
    corp_path=os.path.join(base_path,'corpora')
    foll_path=os.path.join(base_path,'follows')

    os.mkdir(base_path)
    os.mkdir(stat_path)
    os.mkdir(corp_path)
    os.mkdir(foll_path)
    os.mkdir(os.path.join(corp_path,'g'))
    os.mkdir(os.path.join(corp_path,'gc'))

    sample=the_sample(curs)
    
    data=collections.OrderedDict()

    data['g']=collections.OrderedDict()
    data['gc']=collections.OrderedDict()

    print 'Getting data for each genre:'

    print '\tThose who\'ve uploaded tracks...' 
    data['g']['uploaders']=filled_genre_dict(users_by_genre,curs,sample)
    print '\tThe tracks...'
    data['g']['tracks']=filled_genre_dict(tracks_by_genre,curs,sample)
    print '\tAll the comments...'
    data['g']['all_comments']=filled_genre_dict(comments_by_genre,curs,sample)
    print '\tAnd just the English-language comments...'
    data['g']['eng_comments']=filled_genre_dict(comments_by_genre,curs,
                                                sample,True)

    for dict_name in data['g'].keys():
        print 'Writing stats on {} to {}'.format(dict_name,stat_path)
        output_stats(data['g'][dict_name],stat_path,
                     dict_name+'_by_genre')
        data['gc'][dict_name]=genre_community_od(data['g'][dict_name])
        output_stats(data['gc'][dict_name],stat_path,
                     dict_name+'_by_genre_community')

    for dict_name in data.keys():
        print 'Writing English language corpus to {}'.format(corp_path)
        output_corpora(curs,data[dict_name]['eng_comments'],
                       os.path.join(corp_path,dict_name),
                       single_file_corpora)

    print 'Checking follow relationships vis a vis genre...'
    data['f']=following_within_genre(curssourc,curs,
                                     data['g']['uploaders'])
    print 'Writing follow data within {}'.format(foll_path)
    output_follow_stats(data['f'],foll_path)

    return data
