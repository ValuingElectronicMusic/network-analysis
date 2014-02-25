#!/usr/bin/env python

# This is a bunch of functions used for creating a graph representing
# followings in the SoundCloud data, manipulating that graph by removing
# less well-connected nodes, calculating the centrality of nodes to
# the graph, and visualising it. At the end, there's a function called
# 'demonstrate' that shows what some of these things are supposed to
# do.

import networkx as nx  
import pygraphviz as pgv   
import process_scdb_data as pscd

sys_list=['adrift','hugo','inform','tads','zil']

def user_system_dict(users,sys_dict,data):
    '''Returns a dictionary of dictionaries representing users' SoundCloud use.

    To be updated. Keys are users. Values are dictionaries where keys are authoring
    systems and values are integers indicating how many works a
    user has released with each authoring system. 
    NB This is to be converted to keys as genres'''

    sys_used = {}
    for user in users:
        sys_used[user]={}
        for system in sys_list:
            sys_used[user][system] = len(pscd.works_by(user,data)
                                           & sys_dict[system])
    return sys_used

def followings_dict(entities,data):
    '''Returns a dictionary of followings.

    Keys are users, values are agents who followed those users.'''

    return {user:pscd.followers_of_user(user,entities,data) 
            for user in entities.users}

def followings_tuples(followers,users,rec_dict):
    '''Returns a list of tuples representing followings.

    This can be passed directly into a NetworkX digraph object as a
    representation of the graph's arcs.'''

    return [(follower,user) 
            for follower in followers 
            for user in users
            if follower in rec_dict[user]]

def build_network(entities,data,subset=None):
    '''Creates a NetworkX DiGraph object based on followings between
    users.'''

    followers = (entities.followers & subset if subset 
                   else entities.followers)
    users = (entities.users & subset if subset 
               else entities.users)

    g = nx.DiGraph()
    g.add_edges_from(followings_tuples(followers,
                                        users,
                                        followings_dict(entities,data)))

    return g

def reduce_network(g, minimum_incoming=1):
    '''Recursively removes nodes without incoming arcs.

    Useful in that it leaves a graph of users followed by other
    followed users. Note that it doesn't literally do this
    recursively, due to Python's lack of tail call optimisation.'''

    g = g.copy()
    to_drop = [0]
    while to_drop:
        to_drop = [n for n in g.nodes() 
                   if g.in_degree(n) < minimum_incoming]
        g.remove_nodes_from(to_drop)
    return g

def followers_only(g):
    '''Removes nodes without outgoing arcs.

    Useful because it leaves only those nodes that are really
    participating in the network. In the case of my interactive
    fiction data, it gets rid of "historic" users who never used the
    network but are admired by network members.'''

    g = g.copy()
    to_remove = [n for n in g.nodes() 
                 if g.out_degree(n)<1]
    g.remove_nodes_from(to_remove)
    left_over = [n for n in g.nodes() 
                 if g.out_degree(n)<1 and g.in_degree(n)<1]
    g.remove_nodes_from(left_over)
    return g

def draw_network(g,filename,point=True,fac=10,siz=0.2,larger=False):
    '''Represents NetworkX digraph with PyGraphViz AGraph object.

    Extremely kludgy. Note that it gets the layout from the digraph
    object (in the variable 'layout': a dictionary where keys are nodes
    and values are co-ordinates) and sets the 'pos' attribute of each
    node in the AGraph object to the co-ordinates of the corresponding
    node in the digraph object (multiplied by ten to space them
    out).'''

    layout = nx.spring_layout(g)
    ag = pgv.AGraph(directed=True)
    ag.graph_attr['outputorder']='edgesfirst'
    ag.node_attr['fontname']='helvetica'
    ag.node_attr['fixedsize']='true'
    ag.node_attr['fontsize']='8'
    nods = g.nodes(data=True)
    edgs = g.edges(data=True)
    nod_dic = {n[0]:n[1] for n in nods}
    edg_dic = {(e[0],e[1]):e[2] for e in edgs}
    ag.add_nodes_from(g.nodes())
    ag.add_edges_from(g.edges())

    for node in nod_dic:
        a_nod = ag.get_node(node)
        p = layout[node]
        a_nod.attr['pos']='{},{}!'.format(p[0]*fac,p[1]*fac)
        if point: 
            a_nod.attr['shape'] = 'point'
        else: 
            a_nod.attr['shape'] = 'circle'
            a_nod.attr['height']  = str(siz)
            a_nod.attr['style'] = 'filled'
            a_nod.attr['fillcolor'] = 'white'
            a_nod.attr['label'] = ''

    for edge in edg_dic:
        a_edg = ag.get_edge(edge[0],edge[1])
        if point:
            a_edg.attr['arrowsize'] = '0.2'
        else:
            a_edg.attr['arrowsize'] = '0.5'

    ag.layout(prog='neato')
    ag.draw(filename)

    return ag

def centrality_dict_to_list(cd,data):
    return sorted([(y,pscd.name_entity(x,data.agents)) 
                   for x,y in cd.iteritems()])[::-1]

def eigenvector_ranking(g,data):
    g = g.reverse()
    return centrality_dict_to_list(nx.eigenvector_centrality_numpy(g),data)

def pagerank_ranking(g,data):
    return centrality_dict_to_list(nx.pagerank_numpy(g),data)

def in_degree_ranking(g,data):
    return centrality_dict_to_list(g.in_degree(),data)

def demonstrate():
    'This is just there to show how things work. It may take some time.'

    print 'Creating data holder'
    data = pscd.data_holder()

    print 'getting entities from data'
    entities = pscd.entity_holder(data)
    
    print'building network of entities from the data'
    g1 = build_network(entities,data)

    print 'reducing the network'
    g2 = reduce_network(g1)
    
    print 'filtering network to include followers only'
    g3 = followers_only(g2)
    
    print 'drawing the networks, see test1.png, test2.png, test3.png'
    d1 = draw_network(g1,'test1.png') # Extension determines file type.
    d2 = draw_network(g2,'test2.png') # SVG, JPEG, EPS, etc are also
    d3 = draw_network(g3,'test3.png') # possible.

    i_r = in_degree_ranking(g1,data)
    print 'Pos\tName\tIndegree'
    for i in range(10):
        print '{}\t{}\t{}'.format(i+1,i_r[i][1],i_r[i][0])
        
    e_r = eigenvector_ranking(g1,data)
    print 'Pos\tName\tEigenvector'
    for i in range(10):
        print '{}\t{}\t{}'.format(i+1,e_r[i][1],e_r[i][0])
        
    p_r = pagerank_ranking(g1,data)
    print 'Pos\tName\tPageRank'
    for i in range(10):
        print '{}\t{}\t{}'.format(i+1,p_r[i][1],p_r[i][0])
