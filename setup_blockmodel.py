# Intended to be run via execfile. Need to define output_dirpath and
# min_freq and to import gephi_blockmodel as gb before doing
# that. Don't share this on Github; it's just a list of paths on one
# of my Macs.

sample_path='/Users/danielallington/Documents/Research/Electronic_value/data/rs_150_stats/sample.pck'
follows_path='/Users/danielallington/Documents/Research/Electronic_value/data/rs_150_stats/follow_data.pck'
user_data_path='/Users/danielallington/Documents/Research/Electronic_value/data/rs_150_stats/user_data_city_synonyms.pck'
index=4

gb.create_graph(sample_path,follows_path,user_data_path,
                output_dirpath,min_freq,index)
