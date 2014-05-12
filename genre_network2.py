# Create CSV file for correspondence analysis: co-occurrence of genre
# or tag strings

import sqlite3
import csv


def cursor(fn):
    conn=sqlite3.connect(fn)
    return conn.cursor()


def top_strings(curs,table,n):
    strings={}
    c=curs.execute('SELECT string FROM {}'.format(table))
    for i in range(n):
        strings.append(c.next()[0])
    return strings


def user_strings(curs,table):
    return curs.execute('SELECT user,most_used_three FROM {}'.format(table))


def create_csv(db_fn,str_type):

    curs=cursor(db_fn)
    strings=top_strings(curs,str_type,50)

    db_rows=user_strings(curs,'user_{}'.format(str_type))
    csv_rows=[]

    for n,r in enumerate(rows):
        csv_row=[r[0]]
        for s in strings:
            if s in r[1]: csv_row.append(1)
            else: csv_row.append(0)
        csv_rows.append(csv_row)
        if n > 1000: break

    return csv_rows

    print 'Laying out...'
    g.layout()
    print 'Drawing...'
    g.draw(pic_fn)
    return g


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
    g=graph_to_draw(db_fn,pic_fn,'genres')
    print 'Opening...'
    os.system('open {}'.format(pic_fn))
    return g
