import cPickle
import os
import os.path
import glob
import sqlite3
import all_data_one_entity as adoe

list_size_limit=1000

class Writer(object):
    def __init__(self,dir_path,done_file):
        self.trackdir=os.path.join(dir_path,'tracks')
        self.userdir=os.path.join(dir_path,'users')
        self.done_file=done_file
        if not os.path.exists(self.trackdir):
            os.mkdir(self.trackdir)
        if not os.path.exists(self.userdir):
            os.mkdir(self.userdir)
        self.trackstore=[]
        self.userstore=[]
        self.donestore=[]

    def save_and_clear(self,store,dir):
        num=str(len([f for f in os.listdir(dir)])+1)
        f=open(os.path.join(dir,num+'.pck'),'w')
        cPickle.dump(store,f)
        f.close()
        store[:]=[]

    def save_done(self):
        for t in self.donestore:
            self.done_file.write('{}\n'.format(t))
        self.done_file.flush()
        self.donestore[:]=[]

    def save_all(self):
        self.save_and_clear(self.trackstore,self.trackdir)
        self.save_and_clear(self.userstore,self.userdir)
        self.save_done()
        print 'Remainder written.'

    def add_done(self,track):
        self.donestore.append(track)

    def add_track(self,track):
        self.trackstore.append(track)
        if len(self.trackstore) >= list_size_limit:
            print '{} tracks ready to save.'.format(len(self.trackstore))
            self.save_and_clear(self.trackstore,self.trackdir)
            self.save_and_clear(self.userstore,self.userdir)
            self.save_done()

    def add_user(self,user):
        self.userstore.append(user)


def names(listfilepath):
    dir=os.path.dirname(listfilepath)
    name=os.path.basename(listfilepath).split('.')[0]
    subdir=os.path.join(dir,name+'_dir')
    return dir,name,subdir


def get_tracks(listfilepath):
    dir,name,subdir=names(listfilepath)
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    donepath=os.path.join(dir,name+'_done.txt')

    to_do={int(l) for l in open(listfilepath,'r').readlines() if l.strip()}
    if os.path.exists(donepath):
        done_file=open(donepath,'r')
        to_do.difference_update({int(l) for l in done_file.readlines() 
                                 if l.strip()})
        done_file.close()
    to_do=sorted(to_do)

    done_file=open(donepath,'a')
    w=Writer(subdir,done_file)
    
    print '{} to work through...'.format(len(to_do))
    for i,l in enumerate(to_do):
        if i < 10 or i % 1000 == 0: print '{} worked through'.format(i)
        n=int(l)
        td=adoe.track_data(n)
        w.add_done(n)
        if td:
            tu=adoe.user_data(td['user_id'])
            if tu: 
                w.add_user(tu)
            w.add_track(td)

    w.save_all()

def insert_tracks(listfilepath,dbfilepath):
    conn=sqlite3.connect(dbfilepath)
    curs=conn.cursor()
    dir,name,subdir=names(listfilepath)
    tracks=glob.iglob(os.path.join(subdir,'users','*.pck'))
    users=glob.iglob(os.path.join(subdir,'users','*.pck'))
    print 'Tracks now'
    for t in tracks:
        print t
        with open(t) as f:
            l=cPickle.load(f)
            for d in l:
                adoe.insert_into_table(curs,'tracks',d)
    conn.commit()
    print 'Users now'
    for u in users:
        print u
        with open(u) as f:
            l=cPickle.load(f)
            for d in l:
                adoe.insert_into_table(curs,'users',d)
    conn.commit()
    
