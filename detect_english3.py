
import wordsets
import string

# Might be good to do something about respellings. Easiest would be to
# work with repeated letters. The following letters can be double in
# English; none can be triple: e,d,f,l,n,o,p,r,s,t

def get_dic(title):
    with open('dictionaries/'+title+'/'+title+'.dic', 'r') as f:
        return {w.strip() for w in f.readlines()}

engdic=get_dic('en_GB-bncb')

def englishp(t,min_eng):
    wordlist = [w for w in [w.strip(string.punctuation) for w in t.split()] 
                if w]
    engwords = [w for w in wordlist if w in engdic]
    if len(wordlist) == 0: return False
    if len(engwords) / float(len(wordlist)) >= min_eng: return True
    return False


