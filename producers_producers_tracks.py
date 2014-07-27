import sqlite3
import shutil
import time
import os.path
import add_data as ad
import all_data_one_person as adop
import genre_relationships_sample as grs


def get_tracks(curs,user):
    tracks=adop.tracks_by_user(user)
    for track in tracks:
        adop.insert_into_table(curs,'tracks',tracks[track])


def followed_by_sample_producers(curssourc,cursderiv):
    sample={s[0] for s in cursderiv.execute('SELECT user FROM user_genres')}
    return {f[1] for f in curssourc.execute('SELECT follower,followed '
                                            'FROM x_follows_y')
            if f[0] in sample}
    

def users_to_collect(db1,db2,filepath):
    connsourc=sqlite3.connect(db1)
    curssourc=connsourc.cursor()
    connderiv=sqlite3.connect(db2)
    cursderiv=connderiv.cursor()
    print 'Getting users...'
    users=followed_by_sample_producers(curssourc,cursderiv)
    print 'Writing to {}.'.format(filepath)
    with open(filepath,'w') as f:
        for user in sorted(list(users)):
            f.write('{}\n'.format(user))
    return True


def get_processed_filepath(db_path):
    return db_path[:-7]+'_done.txt'


def backup(db_path):
    backup_path='{}_backup_{}.sqlite'.format(db_path[:-7],
                                             time.strftime('%Y%m%d_%H%M'))
    shutil.copyfile(db_path,backup_path)
    shutil.copyfile(get_processed_filepath(db_path),
                    get_processed_filepath(backup_path))


def go_for_it(to_process_filepath,db_path):
    conn=sqlite3.connect(db_path)
    curs=conn.cursor()
    if not grs.check_tables(curs,['tracks'])[0]:
        print 'Creating tracks table.'
        ad.create_table(curs,'tracks')
    with open(to_process_filepath,'r') as to_process:
        users=[int(u.strip('\n')) for u in to_process]
    processed_filepath=get_processed_filepath(db_path)
    if not os.path.exists(processed_filepath):
        f=open(processed_filepath,'w')
        f.close()
    processed=open(processed_filepath,'r')
    for user in processed:
        user=user.strip('\n')
        if user: users.remove(int(user))
    print 'There are {} users to munch through. Here we go!'.format(len(users))
    for n,user in enumerate(users):
        if n % 10000 == 0:
            print 'Backing up...'
            processed.close()
            backup(db_path)
            processed=open(processed_filepath,'a')
        get_tracks(curs,user)
        processed.write('{}\n'.format(user))
        processed.flush() # Otherwise, restart becomes unreliable
        conn.commit()
        if n < 10 or n+1 % 100 == 0: print '{} done.'.format(n+1)
        if n == 10: print 'Only reporting hundreds from now on.'
    print 'Backing up...'
    processed.close()
    backup(db_path)
    print 'And we\'re done.'
    return True

