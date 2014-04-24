# Approximate error rate: 

# Of 1000 comments identified as English, only one was not judged to
# be in English by the programmer (a short comment in Spanish that
# included two English words and some Spanish words that are spelled
# like English words). Harder to quantify what happened with those
# comments not identified as English. For the most part, these were a
# mixture of non-English comments and very short English comments,
# some with non-standard spellings (e.g. 'spooooooky' or 'swagggg!'),
# a small number with non-standard punctuation that confused the
# word-separating algorithm (e.g. 'i-love-this-track'), and a much
# larger number with no lemmas (e.g. the very common
# 'thanks!'). Longer ones missed out tended to be those with few
# lemmas (e.g. 'thanks 4 all great replies guys, really really
# inspires me!'  - 'thanks', 'guys', 'replies', 'really', and
# 'inspires' all have affixes, for example, while '4' and 'me' will
# have appeared in the French dictionary, which left only 'all').

# Overall, not bad. Most regretable problem is a tendency to filter
# out some of the tastiest comments, e.g. 'soooo unhealthy fakkkkk!!!
# dope shit meng'. This would have been picked up if only 'unhealthy'
# were a lemma, but it highlights a bigger problem, i.e. that for
# analytic purposes we really we need a human to identify that 'soooo'
# and 'fakkkkk' are instances of the same lexeme as 'so' and
# 'fuck'. The loss of the very many repetitions of 'thanks' is
# relatively unimportant.

# Note that dictionary of internet terms, e.g. 'omg', 'lol', and
# variants, only added for English.

import wordsets
import string

# Might be good to do something about respellings. Easiest would be to
# work with repeated letters. The following letters can be double in
# English; none can be triple: e,d,f,l,n,o,p,r,s,t

def count_langs(wordlist,langsetsdict):
    d={lang:0 for lang in langsetsdict}
    for word in wordlist:
        for lang in langsetsdict:
            if word in langsetsdict[lang]:
                d[lang] += 1
    return d

def englishp(t,min_eng):
    wordlist = [w for w in [w.strip(string.punctuation) for w in t.split()] 
                if w]
    counted = count_langs(wordlist,wordsets.lang_sets)

    if counted['en'] == 0: return False
    if counted['en'] / float(len(wordlist)) < min_eng: return False
    if counted['en'] < max(v for k,v in counted.items()): return False

    return True


