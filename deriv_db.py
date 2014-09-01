# Small module for functions used by more than one module that works with
# the _deriv.sqlite database.

import sqlite3

def connect_databases(db_source):
    if db_source[-7:]!='.sqlite': db_source=db_source+'.sqlite'
    db_deriv = db_source[:-7]+'_deriv'+db_source[-7:]
    print 'Source: {} \n Deriv: {}'.format(db_source,db_deriv)
    connsourc = sqlite3.connect(db_source)
    connderiv = sqlite3.connect(db_deriv)
    return connsourc,connderiv
