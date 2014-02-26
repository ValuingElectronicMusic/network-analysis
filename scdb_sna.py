#!/usr/bin/env python

# This is a bunch of functions used for creating a graph representing
# recognitions in the IFDB data, manipulating that graph by removing
# less well-connected nodes, calculating the centrality of nodes to
# the graph, and visualising it. At the end, there's a function called
# 'demonstrate' that shows what some of these things are supposed to
# do.

import networkx as nx
import pygraphviz as pgv
import process_ifdb_data as pid

sys_list=['adrift','hugo','inform','tads','zil']

def author_system_dict(authors,sys_dict,data):
    '''Returns a dictionary of dictionaries representing authoring system use.

    Keys are authors. Values are dictionaries where keys are authoring
    systems and values are integers indicating how many works an
    author has released with each authoring system.'''

    sys_used = {}
    for author in authors:
        sys_used[author]={}
        for system in sys_list:
            sys_used[author][system] = len(pid.works_by(author,data)
                                           & sys_dict[system])
    return sys_used

def recognition_dict(entities,data):
    '''Returns a dictionary of recognitions.

    Keys are authors, values are agents who recognised those authors.'''

    return {author:pid.recognisers_of_author(author,entities,data) 
            for author in entities.authors}

def recognition_tuples(recognisers,authors,rec_dict):
    '''Returns a list of tuples representing recognitions.

    This can be passed directly into a NetworkX digraph object as a
    representation of the graph's arcs.'''

    return [(recogniser,author) 
            for recogniser in recognisers 
            for author in authors
            if recogniser in rec_dict[author]]

def build_network(entities,data,subset=None):
    '''Creates a NetworkX DiGraph object based on recognitions between
    creators.'''

    recognisers = (entities.recognisers & subset if subset 
                   else entities.recognisers)
    authors = (entities.authors & subset if subset 
               else entities.authors)

    g = nx.DiGraph()
    g.add_edges_from(recognition_tuples(recognisers,
                                        authors,
                                        recognition_dict(entities,data)))

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

def recognisers_only(g):
    '''Removes nodes without outgoing arcs.

    Useful because it leaves only those nodes that are really
    participating in the network. In the case of my interactive
    fiction data, it gets rid of "historic" authors who never used the
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
    return sorted([(y,pid.name_entity(x,data.agents)) 
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

    data = pid.data_holder()
    entities = pid.entity_holder(data)
    g1 = build_network(entities,data)
    g2 = reduce_network(g1)
    g3 = recognisers_only(g2)
    d1 = draw_network(g1,'test1.png') # Extension determines file type.
    d2 = draw_network(g2,'test2.png') # SVG, JPEG, EPS, etc are also
    d3 = draw_network(g3,'test3.png') # possible.

    i_r = in_degree_ranking(g1,data)
    print 'Pos\tName\tIndegree'
    for i in range(10):
        print '{}\t{}\t{}'.format(i+1,i_r[i][1],i_r[i][0])
