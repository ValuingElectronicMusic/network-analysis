'''
Created on Apr 13, 2014

@author: daniel-allington
'''

# Adds to the _deriv database created in genre_relationships.py with a
# table from which corpora of comments can be pulled. Variables to
# determine whether a given comment will be added to a given corpus
# will be stored in this table too, for the sake of speed later on:
# the commenter's ID and the ID of the person who uploaded the track
# being commented on IF they are in the network of users we've
# collected data on (so that we can build corpora of comments made
# by/on members of particular parts of the social network); booleans
# for whether those two people follow each other assuming that they
# are in the network we have collected (could potentially identify
# comments between people who consider themselves peers? but note that
# it will miss follow relationships, including mutual follow
# relationships, where the commenter or creator was not in the network
# of collected users) and whether the commenter has favourited the
# track he/she is commenting on (could potentially identify positive
# comments... except that none of the comments here were from people
# who'd favourited the tracks in question, but most of the comments
# here are positive); the complete genre and tag_list fields from the
# track (deliberately not processed in any way except for changing to
# lower case - so, unlike with the user_genre and user_tags tables, we
# should use CONTAINS rather than = to search this); the language of
# the comment (identified procedurally, using guess-language - which
# mistakes most of the English comments for other languages but
# fortunately doesn't seem to do the reverse much); the date and time
# when the comment was made (seems a shame to lose it). Then the text
# itself, filtered so that @usernames are replaced by @@ and web
# addresses are replaced by %% (useful preprocessing for corpus
# analysis; note that as the comment IDs are preserved, we can easily
# get the unfiltered text from the original table).

# Technically necessary to load the entire list of comment IDs into
# memory (can't just iterate through the comments table in the
# original database because this would be interrupted by other tasks
# for the cursor). Apart from that, trying to keep as little as
# possible in memory at a time through use of generators.

# Does what it says on the tin now, but some things remain to be
# done. I'd like a more reliable identifier of English language
# comments. And it would be good to have a function that crawled
# through the table and deleted all the spam. We could define spam as
# 'any group of comments with the same text from the same user'.

import re
import deriv_db
import add_data
import guess_language # Needs to be installed from pypi (pip can find it)
import detect_english2

# Regexes for identifying things that will be filtered out of comments

username = re.compile(r'@\S+')
url = re.compile(r'www.\S+|http\S+|\S+\.com|\S+\.co\.\S+')
number = re.compile(r'\d+') # Decided not to use that one in the end.


def corpus_table(cursderiv):
    add_data.create_table(cursderiv,'comments_corp')


def get_comment_ids(curssourc):
    curssourc.execute('SELECT id FROM comments')
    return curssourc.fetchall()

# Duplicate from genre_relationships. Delete, then merge.

def attribute_track(curssourc,track):
    curssourc.execute('SELECT user_id FROM tracks WHERE id=?',(track,))
    u=curssourc.fetchone()
    if u:
        return u[0]
    else:
        return None


def genretags(curssourc,track):
    curssourc.execute('SELECT genre, tag_list FROM tracks WHERE id=?',(track,))
    gt=curssourc.fetchone()
    if gt:
        return ((gt[0].lower() if gt[0] else None),
                (gt[1].lower() if gt[1] else None))
    else:
        return None,None


def filtered(text):
    text=username.sub('@@',text)
    text=url.sub('%%',text)
    return text.lower()


def language(text):
    '''This is the speed bottleneck for the program so we might want to
    lose it. Also, it mistakes most English comments for other
    languages, so I'm not sure it's earning its keep. However, I
    haven't noticed it identifying things as English that weren't, so
    perhaps it should stay.'''
    return guess_language.guessLanguage(text)


def englishp(text):
    '''Looks for a text with at least 50% words to be found in a
    dictionary of English lemmas; to prevent very occasional
    identification of French, Spanish, and Italian comments as
    English, due to loanwords and words that coincidentally have the
    same spelling, also checks that the text does not have a higher
    proportion of words to be found in dictionaries of lemmas in those
    languages. Misidentifies some short English comments as
    non-English, especially where spellings are non-standard or there
    are typing errors. Relies on a union of the OpenOffice
    dictionaries for British and American English - which means we are
    missing inflected forms (e.g. 'really' and 'fucking') because I
    haven't figured out how to parse the affix files. Having scanned a
    couple of thousand positives and negatives, I think I prefer this
    to the above function using guess-language.'''
    return detect_english2.englishp(text,0.5)


def followsp(curssourc,x,y):
    curssourc.execute('SELECT * FROM x_follows_y WHERE follower=? and followed=?',(x,y))
    if curssourc.fetchone(): return True
    else: return False


def favesp(curssourc,x,t):
    curssourc.execute('SELECT * FROM favourites WHERE user_id=? and track_id=?',(x,t))
    if curssourc.fetchone(): return True
    else: return False


def comment_data(curssourc,comment_id_list):
    for id in comment_id_list:
        sql='SELECT body,user_id,track_id,created_at FROM comments WHERE id=?'
        curssourc.execute(sql,(id[0],))
        c=curssourc.fetchone()
        creator=attribute_track(curssourc,c[2])
        x_fol_y=followsp(curssourc,c[1],creator)
        y_fol_x=followsp(curssourc,creator,c[1])
        x_fav_t=favesp(curssourc,c[1],id[0])
        gt=genretags(curssourc,c[2])
        filt=filtered(c[0])
        eng=englishp(filt)
        yield id[0],c[1],creator,x_fol_y,y_fol_x,x_fav_t,gt[0],gt[1],eng,c[3],filt


def add_comment_datum(cursderiv,comment):
    sql='INSERT INTO comments_corp VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    cursderiv.execute(sql,comment)


def add_comment_data(db_source):
    connsourc,connderiv = deriv_db.connect_databases(db_source)
    curssourc=connsourc.cursor()
    cursderiv=connderiv.cursor()
    corpus_table(cursderiv)
    ids = get_comment_ids(curssourc)
    for comment in comment_data(curssourc,ids):
        add_comment_datum(cursderiv,comment)
    connderiv.commit()
