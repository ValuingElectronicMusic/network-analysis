# Create CSV files for network analysis with Gephi, using random sample
# data to create links between nodes representing categories of individuals
# (whether by location or by genre or similar). The code here was based on
# genre_network2.py


import sqlite3
import cPickle
import csv
import os
import collections


city_synonyms={'nyc': 'new york',
               'new york, ny': 'new york',
               'newyork': 'new york',
               'brooklyn': 'new york',
               'bronx': 'new york',
               'montreal': u'montr\u00E9al'.encode('utf-8'),
               'us': None,
               'indonesia': None,
               'england': None,
               'brasil': None,
               'mexico': None,
               u'm\u00E9xico'.encode('utf-8'): None,
               'united kingdom': None,
               'canada': None,
               'national capital region': None,
               'california': None}

the_genres={'hiphop':'urban',
            'rap':'urban',
            'instrumental':'urban',
            'trap':'urban',
            'r&b':'urban',
            'reggae':'urban',
            'beat':'urban',
            'house':'edm',
            'electronic':'edm',
            'dubstep':'edm',
            'techno':'edm',
            'electro':'edm',
            'd&b':'edm',
            'techhouse':'edm',
            'progressivehouse':'edm',
            'dance':'edm',
            'deephouse':'edm',
            'trance':'edm',
            'electrohouse':'edm',
            'hardstyle':'edm',
            'mashup':'edm',
            'ambient':'edm',
            'pop':'other',
            'rock':'other',
            'acoustic':'other',
            'blues':'other',
            'music':'other',
            'cover':'other',
            'folk':'other',
            'jazz':'other',
            'piano':'other',
            'classical':'other',
            'indie':'other',
            'alternative':'other',
            'metal':'other',
            'soundtrack':'other',
            'punk':'other',
            'alternativerock':'other',
            'country':'other',
            'funk':'other',
            'singersongwriter':'other'} # n.b. 'edm' is in the 'edm' group...


def clean_tuple(t,synonyms):
    l=[]
    for i in t:
        try:
            i=(i.encode('utf-8').lower())
            if synonyms:
                try:
                    i=synonyms[i]
                except KeyError:
                    pass
            l.append(i)
        except AttributeError:
            l.append(i)
    return tuple(l)


def get_data(path):
    return cPickle.load(open(path,'rb'))


def get_follows(path,sample):
    f=get_data(path)
    return [t for t in f if t[0] in sample]


def get_users(path,synonyms):
    l1=cPickle.load(open(path,'rb'))
    l2=[clean_tuple(t,synonyms) for t in l1 if t]
    return l2


def nodes_counted(node_data,min_freq):
    nodes_dict=collections.Counter(node_data)
    for n in nodes_dict.keys():
        if nodes_dict[n] < min_freq:
            del(nodes_dict[n])
    return nodes_dict
    

def nodes_csv(nodes_dict):
    rows=[['Id','Label']]
    rows.extend([(k,k) for k in nodes_dict.keys()])
    return rows


def user_dict(user_data,index,nodes):
    print list(user_data)[0]
    return {u[0]:u[index] for u in user_data if u[index] in nodes}


def edges_csv(follow_data,user_data,index,nodes):

    ud=user_dict(user_data,index,nodes)

    edges={}

    for f in follow_data:
        try:
            link=(ud[f[0]],ud[f[1]])
            try:
                edges[link] += 1
            except KeyError:
                edges[link] = 1
        except KeyError:
            pass

    return [('Source','Target','Weight')]+[(k1,k2,v) 
                                           for (k1,k2),v 
                                           in edges.iteritems()]


def write_csv(csv_fn,csv_rows):
    f=open(csv_fn,'wb')
    writer=csv.writer(f,dialect='excel')
    writer.writerows(csv_rows)


def create_graph(sample_path,follows_path,user_data_path,
                 output_dirpath,min_freq,index=4,synonyms=False):
    samp=set(get_data(sample_path))
    print 'Sample: {} ({})'.format(len(samp),
                                   list(samp)[0])
    follows=get_follows(follows_path,samp)
    print 'Follow relationships: {} ({})'.format(len(follows),
                                                 list(follows)[0])
    user_data=get_users(user_data_path,synonyms)
    print 'SoundCloud accounts to process: {} ({})'.format(len(user_data),
                                                           list(user_data)[0])

    nodes=nodes_counted([u[index] for u in user_data 
                         if u[0] in samp
                         and u[index] 
                         and len(u[index])>0],
                        min_freq)
    print 'Nodes: {} ({})'.format(len(nodes),list(nodes)[0])
    write_csv(os.path.join(output_dirpath,'nodes.csv'),
              nodes_csv(nodes))

    edges=edges_csv(follows,user_data,index,set(nodes.keys()))
    print 'Edges: {} ({})'.format(len(edges),list(edges)[0])
    write_csv(os.path.join(output_dirpath,'edges.csv'),
              edges)
    write_csv(os.path.join(output_dirpath,'edges_no_self_loops.csv'),
              [e for e in edges if e[0] != e[1]])
