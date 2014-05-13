# Create CSV file for correspondence analysis: co-occurrence of genre
# or tag strings

import sqlite3
import csv
import codecs


def cursor(fn):
    conn=sqlite3.connect(fn)
    return conn.cursor()


def top_strings(curs,table,n):
    strings=[]
    c=curs.execute('SELECT string FROM {}'.format(table))
    for i in range(n):
        strings.append(c.next()[0])
    return strings


def user_strings(curs,table):
    return curs.execute('SELECT user,most_used_three FROM {}'.format(table))


def binary_csv(db_fn,str_type):

    curs=cursor(db_fn)
    strings=top_strings(curs,str_type,50)

    db_rows=user_strings(curs,'user_{}'.format(str_type))
    binary_rows=[strings]
    sentences=[]

    for n,r in enumerate(db_rows):
        binary_row=[]
        three_strings=r[1].split(' | ')
        strings_used=0
        three_strings_used=[]
        for s in strings:
            if s in three_strings: 
                binary_row.append(1)
                strings_used+=1
                three_strings_used.append(s)
            else: binary_row.append(0)
        if strings_used > 1:
            binary_rows.append(binary_row)
            sentences.append(' '.join(three_strings_used))
#        if n > 100: break

    return binary_rows,sentences

def co_occur_matrix(binary_rows):
    cats=binary_rows[0]
    ncat=len(cats)
    matrix=[[0 for n2 in range(ncat)] for n1 in range(ncat)]
    for n1,row in enumerate(binary_rows[1:]):
        present=[]
        for n2,col in enumerate(row):
            if col==1: present.append(n2)
        for item1 in present:
            for item2 in present:
                if item1 != item2: matrix[item1][item2]+=1
    for n,row in enumerate(matrix):
        row.reverse()
        row.append(cats[n])
        row.reverse()
    matrix.reverse()
    cats.reverse()
    cats.append('')
    cats.reverse()
    matrix.append(cats)
    matrix.reverse()
    return matrix


def write_csv(csv_fn,csv_data):
    f=codecs.open(csv_fn,'wb','utf-8')
    csv_writer = csv.writer(f, delimiter=';',quotechar='"',
                            quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerows(csv_data)


def test():
    dirpath='vis/'
    db_fn='scdb20140501-1106current_deriv'
    for strtype in ['genres','tags']:
        csv_fn='test'+strtype
        binary_data,s=binary_csv(dirpath+db_fn+'.sqlite',strtype)
        matrix_data=co_occur_matrix(binary_data)
        write_csv(dirpath+csv_fn+'_bin.csv',binary_data)
        write_csv(dirpath+csv_fn+'_mat.csv',matrix_data)


def test2():
    dirpath='vis/'
    db_fn='scdb20140501-1106current_deriv'
    for strtype in ['genres','tags']:
        txt_fn='test'+strtype
        binary_data,sentences=binary_csv(dirpath+db_fn+'.sqlite',strtype)
        matrix_data=co_occur_matrix(binary_data)
        with open(dirpath+txt_fn+'.txt','w') as f:
            for s in sentences:
                try:
                    f.write('{}. \n'.format(s))
                except:
                    pass
