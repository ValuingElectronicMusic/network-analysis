# Scripts for finding common strings in the 'genre' and 'tag_list'
# fields. Scrapes data from them with regexes, then interrogates it a
# little. First genres, then tags - the second takes longer to run as
# there are a *lot* more of them. The NLTK is used to identify English
# stopwords: a sledgehammer to crack a nut, but we'll be using it
# anyway for the sentiment analysis.

# And now my reasoning as I was writing the scripts:

# Need to narrow down the huge set of genre entries. This set is
# misleadingly large because multiple genre names may appear in a
# single entry, added to which, capitalisation and spelling are
# inconsistent. Capitalisation is easily fixed. Otherwise, first
# thing is to separate multiple genre names, as best we can. 

# In cases where a double quotation mark is within a genre entry (not
# at the beginning and end), this is a sign that there are multiple
# genre names within the entry (e.g. 'hip hop" "rap'). Single
# quotation marks do not appear to play this role, but do come up in
# phrases like 'rock'n'roll'. Commas can also indicate multiple genres
# (e.g. 'pop,ballad'), but they can also be used in other ways
# (e.g. 'hot, steamy & deep'). Ampersands too, but they appear more
# often in genre names (e.g. 'drum & bass') so best ignore them
# here. Also spaces (e.g. 'soul gospel hillbilly sk8 punk'), but these
# have many other uses, so again best ignore.

# The most common way of indicating multiple genres is with a slash
# (e.g. 'dance/pop'), sometimes also a backslash. Here I will treat
# both kinds of slashes, pairs of double quotation marks, and commas
# as separators. This will lead to some errors (e.g. identification of
# 'hot' and 'steamy & deep' as two separate genres in the previous
# example), but hopefully that's acceptable as we're going to look for
# ones that repeat.

# Tags can be handled more reliably, because they're all enclosed in double
# quotation marks OR are single words.

# Necessary to filter out stopwords like 'the' and 'at' as SoundCloud
# users sometimes include these as tags and genres by mistake.

import sqlite3
import re
import collections
from nltk.corpus import stopwords

stop = stopwords.words('english')

db = 'scdb.sqlite'
conn = sqlite3.connect(db)
curs = conn.cursor()
curs.execute('SELECT genre FROM tracks')
genres = curs.fetchall()
curs.execute('SELECT tag_list FROM tracks')
tags = curs.fetchall()

# Working with genres now

genre_entries = [g[0].lower().strip('"\' ') for g in genres if g[0]]

genre_separators = r'"|,|/|\\'

split_genres = []
for g in genre_entries:
    splits = [p.strip() for p in re.split(genre_separators,g)]
    split_genres.extend([p for p in splits if p])
possib_genres = [g for g in set(split_genres) if g not in stop]

# Search for genre names that are frequent in the 'genre' field

print 'Possible genres frequently appearing in the "genre" field:'

fre = [(len([e for e in split_genres if g==e]),g) for g in possib_genres]
freq = [f for f in (reversed(sorted(fre))) if f[0] > 7] 

for i in range(len(freq)):
    if freq[i][0] < 8: break
    try:
        print '{}\t{}\t{}'.format(i+1,freq[i][1],freq[i][0])
    except UnicodeEncodeError:
        print '{}\t[unprintable]\t{}'.format(i+1,freq[i][0])

s = 0
for g in split_genres:
    contains = 0
    for f in freq:
        if f[1]==g: contains = 1
    s += contains

l = len(genres)

print 'The above appear in {} of {} genre fields ({}%).'.format(s,l,(s/float(l))*100)

blank_gen = len([g for g in genres if not g[0]])

print '{} genre fields ({}%) were blank.'.format(blank_gen,(blank_gen/float(l))*100)

# Now searching for frequent tags

tag_capture = r'"(.+?)"|\b(\S+?)\b'

print 'Frequent tags in the tag list:'

tags = [t[0].lower() for t in tags]
taglists = []
all_tags=[]
for taglist in (tagl for tagl in tags if tagl):
    current_tags = [tag for tag in 
                    [group[0] if group[0] else group[1] 
                     for group in re.findall(tag_capture,taglist)] 
                    if len(tag)>1 and tag not in stop]
    taglists.append(current_tags)
    all_tags.extend(current_tags)
possib_tags = set(all_tags)

tfre = [(len([tl for tl in taglists if t in tl]),t) for t in possib_tags]
tfreq = [f for f in (reversed(sorted(tfre))) if f[0] > 49] 

for i in range(len(tfreq)):
    if tfreq[i][0] < 8: break
    try:
        print '{}\t{}\t{}'.format(i+1,tfreq[i][1],tfreq[i][0])
    except UnicodeEncodeError:
        print '{}\t[unprintable]\t{}'.format(i+1,tfreq[i][0])

ts = 0
for taglist in taglists:
    contains = 0
    for tf in tfreq:
        if tf[1] in taglist: contains = 1
    ts += contains

tl = len(tags)

print 'The above appear in {} of {} tag lists ({}%).'.format(ts,tl,(ts/float(tl))*100)

blank_tag = len([t for t in tags if not t])

print '{} tag lists ({}%) were blank.'.format(blank_tag,(blank_tag/float(tl))*100)
