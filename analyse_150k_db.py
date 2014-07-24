import genre_relationships_sample as grs

filepath='/Users/danielallington/Documents/Research/Electronic_value/data/rand_samp_150k.sqlite'

def do_it():
    grs.gt_tables(filepath)
    grs.user_gt_tables(filepath)
    grs.user_frequency_tables(filepath)

