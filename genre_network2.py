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


def top_strings(curs,table,min_frequency,include_frequency):
    strings=[]
    curs.execute('SELECT string,frequency FROM {}'.format(table))
    from_table = curs.fetchall()
    for t in from_table:
        if t[1] < min_frequency: break
        if not include_frequency:
            strings.append(t[0])
        else:
            strings.append(t)
    return strings


def user_strings(curs,table):
    return curs.execute('SELECT most_used_three FROM {}'.format(table))


def nodes_csv(db_fn,str_type,min_frequency):

    curs=cursor(db_fn)
    rows=[['Id','Label','Size']]
    rows.extend([[a[0],a[0],a[1]] for a in 
                 top_strings(curs,str_type[:-1]+'_popularity',
                             min_frequency,True)])
    return rows


def edges_csv(db_fn,str_type,min_frequency):

    curs=cursor(db_fn)
    strings=top_strings(curs,str_type[:-1]+'_popularity',min_frequency,False)

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
            if total > 0:
                string_assoc_norm[s1][s2]=int((string_assoc[s1][s2]/float(total))*100)
            else:
                string_assoc_norm[s1][s2]=0

    matrix=[['']+strings]
    edges=[['Source','Target','Weight','Type']]
    norm_matrix=matrix[:]
    norm_edges=edges[:]

    for s1 in strings:
        mat_row = [s1]
        norm_mat_row = [s1]
        for s2 in strings:
            weight = string_assoc[s1][s2]
            norm_weight = string_assoc_norm[s1][s2]
            mat_row.append(weight)
            norm_mat_row.append(norm_weight)
            if weight > 0 and [s2,s1,weight,'Undirected'] not in edges:
                # Don't count edge weight twice for undirected graph
                edges.append([s1,s2,weight,'Undirected'])
            if norm_weight > 0: 
                norm_edges.append([s1,s2,norm_weight,'Directed'])
        matrix.append(mat_row)
        norm_matrix.append(norm_mat_row)

    return matrix, norm_matrix, edges, norm_edges


def utf_encode_cell(csv_cell):
    if type(csv_cell) is int:
        return csv_cell
    else:
        return csv_cell.encode('utf-8')


def utf_encode_row(csv_row):
    return [utf_encode_cell(csv_cell) for csv_cell in csv_row]


def utf_encode_rows(csv_rows):
    return [utf_encode_row(csv_row) for csv_row in csv_rows]


def write_csv(csv_fn,csv_rows):
    f=open(csv_fn,'wb')
    writer=csv.writer(f,dialect='excel')
    writer.writerows(utf_encode_rows(csv_rows))


def make_network(db_fn,csv_fn,str_type,min_frequency):
    nodes=nodes_csv(db_fn,str_type,min_frequency)
    matrix,norm_matrix,edges,norm_edges=edges_csv(db_fn,str_type,min_frequency)
    print 'writing nodes'
    write_csv(csv_fn+'_nodes.csv',nodes)
    print 'writing raw matrix'
    write_csv(csv_fn+'_raw_matrix.csv',matrix)
    print 'writing normalised matrix'
    write_csv(csv_fn+'_normalised_matrix.csv',norm_matrix)
    print 'writing weighted edge list'
    write_csv(csv_fn+'_raw_edges.csv',edges)
    print 'writing normalised weighted edge list'
    write_csv(csv_fn+'_normalised_edges.csv',norm_edges)
