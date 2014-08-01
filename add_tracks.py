import sqlite3
import add_data

def swap_em_in(source,target):
    connsourc=sqlite3.connect(source)
    conntarge=sqlite3.connect(target)
    curssourc=connsourc.cursor()
    curstarge=conntarge.cursor()
    att_str=add_data.att_string(add_data.tables['tracks'])
    att_lst=add_data.att_list(att_str)
    sql1='SELECT * FROM tracks'
    sql2=('INSERT INTO tracks ({}) '
          'VALUES({})'.format(att_str,('?, '*len(att_lst))[:-2]))
    done=0
    for n,datum in enumerate(curssourc.execute(sql1)):
        try:
            curstarge.execute(sql2,datum)
            done += 1
        except sqlite3.IntegrityError:
            pass
        if n % 500 == 0: print 'Tried: {}'.format(n)
        if done > 0 and done % 500 == 0: 
            print 'Done: {}'.format(done)
            conntarge.commit()
    conntarge.commit()
    return True
