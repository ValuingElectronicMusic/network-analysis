# Create CSV file for import into Gephi

import sqlite3
import csv
import codecs
import collections

seph_city_codes=['london','bristol','berlin','los angeles','new york']
curs_city_codes=['london','berlin','budapest','glasgow','leipzig']
shir_city_codes=['london','amsterdam','los angeles','paris','sheffield']
slac_city_codes=['london','bristol','manchester','paris','berlin']

def cursor(db_fn):
    conn=sqlite3.connect(db_fn+'.sqlite')
    return conn.cursor()


def write_csv(fn,csv_data):
    f=codecs.open(fn,'wb','utf-8')
    csv_writer = csv.writer(f, delimiter=';',
                            quoting=csv.QUOTE_NONE)
    csv_writer.writerows(csv_data)


def cities(curs,to_include):
    c=curs.execute('SELECT id,city FROM users')
    cits=collections.Counter((u[1] for u in c if u[0] in to_include))
    return cits.most_common()  


def node_csv(curs,to_include):
    yield 'Id','Modularity Class'
    c=curs.execute('SELECT id, city FROM users')
    print 'Working through nodes now...'
    for n,u in enumerate(c):
        if n % 10000 == 0: print '{} checked.'.format(n)
        if u[0] in to_include:
            city=0
            if u[1]:
                for n,c in enumerate(city_codes):
                    if c in u[1].lower():
                        city=n+1
            yield u[0],city


def edge_csv(curs,to_include):
    yield 'Source','Target'
    c=curs.execute('SELECT follower, followed FROM x_follows_y')
    print 'Working through edges now...'
    for n,f in enumerate(c):
        if n % 10000 == 0: print '{} checked.'.format(n)
        if f[0] in to_include and f[1] in to_include:
            yield f[0],f[1]


def csv_files(db_fn,csv_fn,to_include):
    curs=cursor(db_fn)
    node_fn=csv_fn+'_nodes.csv'
    print 'Writing nodes...'
    write_csv(node_fn,node_csv(curs,to_include))
    edge_fn=csv_fn+'_edges.csv'
    print 'Writing edges...'
    write_csv(edge_fn,edge_csv(curs,to_include))


def waves(db_fn,seed,n):
    curs=cursor(db_fn)
    include = set([])
    for wave in range(n):
        table='from_{}_degree_{}'.format(seed,wave)
        sql = 'SELECT id FROM {}'.format(table)
        print sql
        curs.execute(sql)
        for u in curs.fetchall():
            include.add(u[0])
    return include


def test():
    writepath='vis/'
    readpath='minim/data/'
    db_fn='ego_net_of_slackk'
    csv_fn='follows_slackk'
    to_include=waves(readpath+db_fn,202195,2)
    print 'To include: {}'.format(len(to_include))
    csv_files(readpath+db_fn,writepath+csv_fn,to_include)

