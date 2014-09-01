

import sqlite3
import collections
import csv
import os.path
import cPickle
import time
import numpy   # Originally used statlib but its median function is buggy
import deriv_db
import gephi_blockmodel as gb


headings=[('','',
           'Followers','','',
           'Following','','',
           'Tracks','',''),
          ('','n')+('Mean','Median','StDev')*3]


def sample(curs):
    l=set([])
    t=time.time()
    for c in curs.execute('SELECT id FROM sample'):
        l.add(c[0])
    print '\t{} grabbed in {} sec'.format(len(l),int(time.time()-t))
    return l 


def user_data(curs):
    l=set([])
    t=int(time.time())
    for c in curs.execute('SELECT id,followers_count,followings_count,'
                          'track_count,city,country FROM users'):
        l.add(c)
        if len(l) % 10000==0: 
            print '\tGrabbed: {} ({} sec)'.format(len(l),int(time.time())-t)
            t=int(time.time())
    return l 


def uploaders(data):
    return {d[0] for d in data if d[3] > 0}


def follows(curs):
    l=set([])
    for c in curs.execute('SELECT follower,followed FROM x_follows_y'):
        l.add(c)
        if len(l) < 10 or len(l) % 10000==0: print '\tGrabbed: {}'.format(len(l))
    return l


def cities(data):
    return [c[:4]+(c[4].encode('utf-8'),) for c in data if c[4]]


def countries(data):
    return [c[:4]+(c[5].encode('utf-8'),) for c in data if c[5]]


def genres(data,cursderiv,restrict=False):
    cursderiv.execute('SELECT user,most_used FROM user_genres '
                      'WHERE most_used IS NOT NULL')
    if restrict:
        g = {gu for gu in cursderiv.fetchall() if gu[0] in restrict}
    else:
        g = {gu for gu in cursderiv.fetchall()}
    return [(user[0:4]+(ugen[1].encode('utf-8'),)
             for user in data if user[0]==ugen[0]).next()
            for ugen in g]


def popular_choices(l):
    return collections.Counter([i[1] for i in l]).most_common()


def round(n):
    return int(n+0.5)


def statistics(l):
    if len(l) == 0 or sum(l) == 0: return 0,0,0
    elif len(l) == 1: return l[0],l[0],0
    else:
        return (round(numpy.mean(l)),
                round(numpy.median(l)),
                round(numpy.std(l)))


def all_stats(input,restrict=False,start=1,finish=4):
    try:
        l=[i for i in input if i[0] in restrict]
    except TypeError:
        l=input
    data=()
    for n in range(start,finish):
        data=data+statistics([i[n] for i in l])
    return (len(l),)+data


def stats_by_choice(l,restrict):
    data={}
    for c in {i[4] for i in l}:
        data[c]=[i for i in l if i[4]==c]
    return data


def output_stats(l,path,name):
    with open (os.path.join(path,name+'.csv'),'wb') as f:
        writer=csv.writer(f,dialect='excel')
        writer.writerows(l)


def vital_stats(input,samp,samp_uplo,foll_samp,foll_samp_uplo):
    data=headings[:]
    data.append(('Whole sample',)+
                all_stats(input,samp))
    data.append(('Uploaders only',)+
                all_stats(input,samp_uplo))
    data.append(('Followed by whole sample',)+
                all_stats(input,foll_samp))
    data.append(('Followed by uploaders',)+
                all_stats(input,foll_samp_uplo))
    return data


def choice_stats(input,restrict):
    data=reversed(sorted([(c,)+all_stats(l,restrict) 
                          for c,l 
                          in stats_by_choice(input,restrict).iteritems()],
                         key=lambda x: x[1]))
    return headings[:]+list(data)


def save_data(data,output_path,fn):
    f=open(os.path.join(output_path,fn+'.pck'),'wb')
    cPickle.dump(data,f)
    f.close()


def prepare(db_path='/Users/danielallington/Documents/Research/Electronic_value/data/ten_users.sqlite',
            output_path='/Users/danielallington/Documents/Research/Electronic_value/data/rs_stats_test'):
    connsourc,connderiv=deriv_db.connect_databases(db_path)
    curssourc=connsourc.cursor()
    cursderiv=connderiv.cursor()

    print 'Getting data...'
    data=sample(curssourc)
    print 'Got sample.' 
    save_data(data,output_path,'sample')

    print 'Getting user data...'
    data=user_data(curssourc)
    print 'Got user data.'
    save_data(data,output_path,'user_data')

    print 'Getting follows...'
    data=follows(curssourc)  
    print 'Got follows.'
    save_data(data,output_path,'follow_data')
    print 'Okay, we\'re done.'
    

def go(data,folls,
       db_path='/Users/danielallington/Documents/Research/Electronic_value/data/rand_samp_150k_tracks_boost2.sqlite',
       output_path='/Users/danielallington/Documents/Research/Electronic_value/data/rs_150_stats/cleaned'):
    connsourc,connderiv=deriv_db.connect_databases(db_path)
    curssourc=connsourc.cursor()
    cursderiv=connderiv.cursor()

    print 'Getting sample...'

    samp=sample(curssourc)
    print 'Got sample. Separating out users...'
    #    data=user_data(curssourc)

    uplo=uploaders(data)
    samp_uplo=samp & uplo

    print 'Separated out. Figuring out who\'s following who...'
    foll_samp={f[1] for f in folls if f[0] in samp}
    foll_samp_uplo={f[1] for f in folls if f[0] in samp_uplo}

    print 'Figured. Ready to go...'

    print 'Doing overall stats...'

    output_stats(vital_stats(data,samp,samp_uplo,
                             foll_samp,foll_samp_uplo),
                 output_path,'basic')

    print 'Losing unnecessary data...'

    del(uplo)
    del(folls)
    del(foll_samp)
    del(foll_samp_uplo)
    data={d for d in data if d[0] in samp}

    print 'Lost. Now doing breakdown by city, country, and genre...'

    for str1,func in [('cities',cities),
                      ('countries',countries)]:
        for str2,restrict in [('sample',samp),
                              ('sample_uploaders',samp_uplo)]:
            filtered_data=func(data)
            fn='{}_{}'.format(str2,str1)
            save_data(filtered_data,output_path,fn)
            output_stats(choice_stats(filtered_data,restrict),
                         output_path,fn)

    filtered_data=genres(data,cursderiv,samp_uplo)
    save_data(filtered_data,output_path,'sample_uploaders_genres')
    output_stats(choice_stats(filtered_data,samp_uplo),
                 output_path,'sample_uploaders_genres')

    print 'Done.'


def genre_locales(gen_file,loc_file,gen_list,output_path):
    gen_users=[gu for gu in gen_file if gu[4] in set(gen_list)]
    gen_loc_users_dict={g:set([]) for g in gen_list}
    for lu in loc_file:
        for gu in gen_users:
            if lu[0]==gu[0]:
                gen_loc_users_dict[gu[4]].add(lu[0])
                break
    output=headings[:]
    for g in gen_list:
        output.append((g,)+('',)*9)
        output.extend(choice_stats(loc_file,gen_loc_users_dict[g])[2:6])
    output_stats(output,output_path,'genre_locales')


def make_user_data_dict(user_data):
    return {u[0]:gb.clean_tuple(u[1:],gb.city_synonyms) for u in user_data}


def location_follows(sample,follows,user_data_dict):
    followed_by_sample={s:[0,0,0,0] for s in sample}
    followers_of_sample={s:[0,0,0,0] for s in sample}
    print '{} follow relationships to process...'.format(len(follows))
    for n,f in enumerate(follows):
        if n % 100000 == 0: print '{} done'.format(n)
        for tally,index in [(followed_by_sample,0),(followers_of_sample,1)]:
            try:
                l=tally[f[index]]
                follower=user_data_dict[f[0]]
                followed=user_data_dict[f[1]]
            except KeyError:
                continue
            if follower[3] and followed[3]:
                l[0]+=1
                if follower[3]==followed[3]:
                    l[1]+=1
            if follower[4] and followed[4]:
                l[2]+=1
                if follower[4]==followed[4]:
                    l[3]+=1

    return followed_by_sample,followers_of_sample


def round_float(n):
    return int(n+0.5)


def percentage(x,y):
    if y==0: return None
    return round_float((x / float(y)) * 100)


def loc_user_list(loc_user_dict,user_data_dict):
    return [(user_data_dict[k][3],v[0],percentage(v[1],v[0]),
             user_data_dict[k][4],v[2],percentage(v[3],v[2])) 
            for k,v in loc_user_dict.iteritems()]


def loc_follow_dict(l,index):
    locs={i[index]:[] for i in l}
    if None in locs: del(locs[None])
    for i in l:
        if i[index]:
            locs[i[index]].append((i[index+1],i[index+2]))
    return locs


def loc_follow_stats(dict):
    return list(reversed(sorted([(loc,)+all_stats([i for i in dict[loc] 
                                                   if i[0]>0],False,0,2)
                            for loc in dict.keys()],key=lambda x: x[1])))


def head_loc_follow_stats(l,loc_type,rel_type):

    return [('','',
             '{} with {} listed'.format(rel_type,loc_type),'','',
             '% within same {}'.format(loc_type),'',''),
            ('','n')+('Mean','Median','StDev')*2]+l


def do_loc_follow_stats(sample,follows,user_data_dict,path):
    lf=location_follows(sample,follows,user_data_dict)
    for x,rel_type in enumerate(['Follows','Followers']):
        for n,loc_type in [(0,'city'),(3,'country')]:
            d=loc_follow_dict(loc_user_list(lf[x],user_data_dict),n)
            l=loc_follow_stats(d)
            the_stats=head_loc_follow_stats(l,
                                            loc_type,rel_type)

            output_stats(the_stats,path,'{}_{}'.format(rel_type,loc_type))

