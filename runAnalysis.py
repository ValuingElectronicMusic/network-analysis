'''
Created on 21 Feb 2014

@author: annaj
'''

def main(): 
    import ifdb_sna as isna
    import process_ifdb_data as pifdata
    import soundcloud 

    client = soundcloud.Client(client_id='3d158f3620682a747df5e90bb3309b2e')

    print 'Demonstrating process_ifdb_data'
    pifdata.demonstrate()
    print 'Demonstrating ifdb_sna'
    demo = isna.demonstrate()

    tracks = client.get('/tracks', limit=10)
    print 'Ten tracks'
    for track in tracks: 
        print track.title
    app = client.get('/apps/124')
    print 'app permalink url '
    print app.permalink_url
    
    track = client.get('/tracks/30709985')
    print 'title of the specific track'
    print track.title    

    print 'resolve track calumbowen/winnose-the-calm-before-the and print id'
    track = client.get('/resolve', url='https://soundcloud.com/calumbowen/winnose-the-calm-before-the')
    print track.id