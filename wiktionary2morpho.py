import sys
import random

forms2analyses = {}

filename = sys.argv[1]
pos = "NOUN" if "noun" in filename else "VERB" if "verb" in filename else ""
merge = "merge" in sys.argv

with open(filename) as f:
    for line in f:
        line = line.strip()
        if not merge:
            form, lemma, analysis = line.split(",")
        else:
            form, analysis = line.split("\t")
#        form = form.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
        if form not in forms2analyses:
            forms2analyses[form] = []
        if not merge:
            forms2analyses[form].append(pos + " " + " ".join(analysis.split(":")))
#            forms2analyses[form,pos].append(' '.join(analysis.split(':')))
        else:
            forms2analyses[form].append(analysis)
        #result = " ".join(form.lower()) + "\t" + pos # + " ".join(lemma)
        #for feature in analysis.split(":"):
        #    k, v = feature.split("=")
        #    result += v.upper() + " "
        #print(result.strip())

forms = list(forms2analyses.keys())
random.shuffle(forms)

for form in forms:
    _as = forms2analyses[form]
    if not merge:
        print(' '.join(list(form.lower())) + '\t' + ' ; '.join(_as))

    else:
        print(form + '\t' + ' ; '.join(_as))
