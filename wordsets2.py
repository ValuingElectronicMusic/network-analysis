import re
import itertools

# Produces a set of lemmas for each of four languages: English,
# Spanish, French, Italian. This because we're trying to detect
# English from presence of particular words, and the other three were
# the languages that got mistaken for it in tests (e.g. 'prima o poi
# verro` a sentirti dal vivo..bella bella musica..' was classified as
# English in an earlier version of the algorithm that only looked for
# 50% 'English' words: 'prima', 'o', 'a', 'dal', 'vivo', and 'bella'
# are all in the English dictionary). Sets of lemmas stored in a
# dictionary called lang_sets.

# Lemmas mostly extracted from OpenOffice spellcheck dictionaries
# downloaded from
# http://archive.services.openoffice.org/pub/mirror/OpenOffice.org/contrib/dictionaries/
# Exception is the en_WW.dic file, created from the Wiktionary list
# of English internet terms

# Inflected forms not included. It would be better if they were
# included, since some are very common in the data (e.g. 'really'),
# but at the moment it's too much work to extract them from the
# OpenOffice files above. Better solution longterm might be to use
# e.g. the most common 3000 written words for each language from
# a reliable corpus (in part because letter combinations present in
# more than one language are usually rarer in one than the others,
# e.g. 'para' is a common Spanish word but a rare English one). I can
# easily get that for English, but not at home as I don't have any
# good corpora installed.

langs = {'en':['en_GB','en_GB-oed','en_US','en_WWW','en_EDM'],
         'es':['es_ES'],
         'fr':['fr_FR'],
         'it':['it_IT']}

sep = re.compile(r'\\|/')
roman = re.compile('[a-z]')

def get_dic(title):
    with open('dictionaries/'+title+'/'+title+'.dic', 'r') as f:
        return f.readlines()


def lemmas(l):
    return [w for w in [sep.split(w)[0].lower().strip() for w in l] 
            if roman.search(w)]


def lang_set(lang):
    return {i for i in itertools.chain(*[lemmas(get_dic(title)) 
                                         for title in lang])}


lang_sets = {lang:lang_set(langs[lang]) for lang in langs}

