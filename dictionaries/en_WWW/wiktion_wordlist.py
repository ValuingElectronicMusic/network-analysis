import re

r = re.compile(r'title=".+">(\S+)</a></b>: .+</li>')

f=open('Appendix - English internet slang - Wiktionary.html','r')
t=f.read()
f.close()

def scrape():
    return r.findall(t)

missed=['a/s/l','a/s/l/p','ayb','bbl','dilligad','dilligas','gtg','haxor',
        'h4x0r','jk','k','newbie','newb','n/m','nvm','nvmd','rly','pebkac',
        'rehi','re','rofl','roflmao','roflmaowpimp','roflol','rtfm','sk8',
        'sk8r','timwtk','thx','thnx','tnx','w00t','w/']

missing=['gnarly','ha','haha','hahaha','hahahaha','rawr','remix',
         'zomfg']

def terms():
    return {t.lower() for t in scrape()} | set(missed) | set(missing)

def make_dic():
    t=terms()
    f=open('en_WWW.dic','w')
    f.write(str(len(t))+'\n'+'\n'.join(sorted(t)))
    f.close()
