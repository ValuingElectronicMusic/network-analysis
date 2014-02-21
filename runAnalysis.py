'''
Created on 21 Feb 2014

@author: annaj
'''

def main(): 
    import ifdb_sna as isna
    import process_ifdb_data as pifdata

    print 'Demonstrating process_ifdb_data'
    pifdata.demonstrate()
    print 'Demonstrating ifdb_sna'
    demo = isna.demonstrate()