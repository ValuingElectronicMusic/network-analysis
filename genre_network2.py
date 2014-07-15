# Create two CSV files for network analysis with Gephi: node size
# defined by number of individuals with that string as their most
# frequent one; edges by number of individuals with any particular
# pair in their most frequent three.

import sqlite3
import csv
import collections


def cursor(fn):
    conn=sqlite3.connect(fn)
    return conn.cursor()


def top_strings(curs,table,n,include_frequency):
    strings=[]
    c=curs.execute('SELECT string,frequency FROM {}'.format(table))
    for i in range(n):
        if not include_frequency:
            strings.append(c.next()[0])
        else:
            strings.append(list(c.next()))
    return strings


def user_strings(curs,table):
    return curs.execute('SELECT most_used_three FROM {}'.format(table))


def nodes_csv(db_fn,str_type):

    curs=cursor(db_fn)
    rows=[['Id','Label','Size']]
    rows.extend([[a[0],a[0],a[1]] for a in 
                 top_strings(curs,str_type[:-1]+'_popularity',50,True)])
    return rows


def edges_csv(db_fn,str_type):

    curs=cursor(db_fn)
    strings=top_strings(curs,str_type[:-1]+'_popularity',50,False)

    db_rows=user_strings(curs,'user_{}'.format(str_type))

    string_assoc=collections.defaultdict(dict)

    for s1 in strings:
        for s2 in strings:
            string_assoc[s1][s2]=0

    for trio in db_rows:
        trio=[s.strip() for s in trio[0].split('|')]
        for s1 in strings:
            if s1 in trio:
                for s2 in strings:
                    if s2 != s1 and s2 in trio:
                        string_assoc[s1][s2]+=1
            
    string_assoc_norm=collections.defaultdict(dict)

    for s1 in strings:
        total = sum([v for k,v in string_assoc[s1].items()])
        for s2 in strings:
            string_assoc_norm[s1][s2]=int((string_assoc[s1][s2]/float(total))*100)

    matrix=[['']+strings]
    edges=[['Source','Target','Weight','Type']]
    norm_matrix=matrix[:]
    norm_edges=edges[:]

    for s1 in strings:
        mat_row = [s1]
        norm_mat_row = mat_row[:]
        for s2 in strings:
            weight = string_assoc[s1][s2]
            norm_weight = string_assoc_norm[s1][s2]
            mat_row.append(weight)
            norm_mat_row.append(norm_weight)
            if weight > 0: 
                edges.append([s1,s2,weight,'Undirected'])
            if norm_weight > 0: 
                norm_edges.append([s1,s2,norm_weight,'Directed'])
        matrix.append(mat_row)
        norm_matrix.append(norm_mat_row)

    return matrix, norm_matrix, edges, norm_edges


def write_csv(csv_fn,csv_rows):
    f=open(csv_fn,'wb')
    writer=csv.writer(f,dialect='excel')
    writer.writerows(csv_rows)


def make_genre_network(db_fn):
    nodes=nodes_csv(db_fn)
    matrix,norm_matrix,edges,norm_edges=edges_csv(db_fn)
    write_csv(csv_fn+'_nodes.csv',nodes)
    write_csv(csv_fn+'_raw_matrix.csv',matrix)
    write_csv(csv_fn+'_normalised_matrix.csv',norm_matrix)
    write_csv(csv_fn+'_raw_edges.csv',edges)
    write_csv(csv_fn+'_normalised_edges.csv',norm_edges)
