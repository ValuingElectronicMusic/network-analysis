import genre_relationships_sample as grs
import genre_work as gw
import comments_corp as cc

def do_it():
    db='/Users/danielallington/Documents/Research/Electronic_value/data/rand_samp_150k_tracks_boost2.sqlite'
    print 'Copying tables across'
    grs.copy_tables_across(db)
    print 'Doing gt tables'
    grs.gt_tables(db,True)
    print 'Doing user gt tables'
    grs.user_gt_tables(db,False)
    print 'Doing comments corp'
    cc.add_comment_data(db)
    print 'Producing stats & corpora'
    gw.do_everything(db,True)
