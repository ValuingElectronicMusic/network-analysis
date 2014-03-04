#!/usr/bin/env python

# This is a bunch of functions used for creating a graph representing
# recognitions in the IFDB data, manipulating that graph by removing
# less well-connected nodes, calculating the centrality of nodes to
# the graph, and visualising it. At the end, there's a function called
# 'demonstrate' that shows what some of these things are supposed to
# do.

import networkx as nx
import pygraphviz as pgv
import process_scdb_data as pscd


def build_network(entities,data,subset=None):
    '''Creates a NetworkX DiGraph object based on recognitions between
    creators.'''

    g = nx.DiGraph()
    g.add_edges_from(data.x_follows_y)
    return g

def reduce_network(g, minimum_incoming=1):
    '''Recursively removes nodes without incoming arcs.

    Useful in that it leaves a graph of creators recognised by other
    recognised creators. Note that it doesn't literally do this
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
    participating in the network. In the case of the SoundCloud
    data, it gets rid of "historic" users who never used the
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
    return sorted([(y,pscd.getUserName(x,data.users)) 
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

    data = pscd.data_holder()
    pscd.printData(data)
    entities = pscd.entity_holder(data)
    pscd.printEntities(entities)
    g1 = build_network(entities,data)
    g2 = reduce_network(g1)
    g3 = followers_only(g2)
    d1 = draw_network(g1,'graph_full_network.png') # Extension determines file type.
    d2 = draw_network(g2,'graph_reduced_network.png') # SVG, JPEG, EPS, etc are also
    d3 = draw_network(g3,'graph_reduced_and_followers_only.png') # possible.

    print ''
    i_r = in_degree_ranking(g1,data)
    print 'Pos\tName\tIndegree'
    for i in range(len(i_r)-1):
        #print '{}\t{}\t{}'.format(i+1,i_r[i][1],i_r[i][0])
        print(str(i+1)+'\t'+i_r[i][1]+'\t'+str(i_r[i][0]))
    
    print ''
    e_r = eigenvector_ranking(g1,data)
    print 'Pos\tName\tEigenvector'
    for i in range(len(e_r)-1):
        print(str(i+1)+'\t'+e_r[i][1]+'\t'+str(e_r[i][0]))
    
    print ''
    p_r = pagerank_ranking(g1,data)
    print 'Pos\tName\tPageRank'
    for i in range(len(p_r)-1):
        print(str(i+1)+'\t'+p_r[i][1]+'\t'+str(p_r[i][0]))