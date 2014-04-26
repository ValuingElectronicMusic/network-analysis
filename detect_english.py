import wordsets
import string

def count_langs(wordlist,langdict):
    d={lang:0 for lang in langdict}
    for word in wordlist:
        for lang in langdict:
            if word in lang:
                d[lang] += 1
        return len([w for w in l if w in eng_words])

def englishp(t,min_eng):
    l = [w for w in [w.strip(string.punctuation) for w in t.split()] if w]
    try:
        if count_english(l) / float(len(l)) >= min_eng: return True
    except ZeroDivisionError:
        pass
    return False

