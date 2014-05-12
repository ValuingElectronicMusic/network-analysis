# Create, visualise, and analyse undirected (but implicitly directed)
# bipartite graph of individuals and the genres or tags that they most
# commonly use for their tracks.

import networkx as nx
import pygraphviz as pgv
import sqlite3
import os

def cursor(fn):
    conn=sqlite3.connect(fn)
    return conn.cursor()


def top_strings(curs,table,n):
    strings={}
    c=curs.execute('SELECT string FROM {}'.format(table))
    for i in range(n):
        strings[c.next()]=i+1
    return strings


def user_strings(curs,table):
    return curs.execute('SELECT user,most_used_three FROM {}'.format(table))


def graph_to_draw(db_fn,pic_fn,str_type):
    '''Creates an undirected PyGraphviz AGraph object based on use of
    genres/tags.'''

    curs=cursor(db_fn)

    strings=top_strings(curs,str_type,50)
    g = pgv.AGraph()
    g.graph_attr['outputorder']='edgesfirst'
    g.node_attr['fontname']='helvetica'
    g.node_attr['fixedsize']='true'
    g.node_attr['fontsize']='8'

    for k,v in strings.iteritems():
        g.add_node(k,shape='circle',style='filled',fillcolor='white',
                   label=v)

    rows=user_strings(curs,'user_{}'.format(str_type))
    n=0
    for r in rows:
        linked=False
        for k in strings:
            if k[0] in r[1]: 
                if not linked:
                    g.add_node(r[0],shape='point',color='white',label='')
                    linked=True
                g.add_edge(r[0],k)
        print n
        n+=1
        if n > 1000: break

    print 'Laying out...'
    g.layout()
    print 'Drawing...'
    g.draw(pic_fn)


def betweenness_ranking(g):
    pass
#    return nx.betweenness_centrality_numpy(g)


def graph_to_analyse(s,tuples):
    '''Creates a NetworkX Graph object based on use of genres/tags.'''
    s = top_strings
    g = nx.Graph()
    g.add_edges_from(tuples)
    return g


def test():
    db_fn='vis/scdb20140501-1106current_deriv.sqlite'
    pic_fn='vis/test.png'
    graph_to_draw(db_fn,pic_fn,'genres')
    print 'Opening...'
    os.system('open {}'.format(pic_fn))
