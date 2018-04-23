import sys


forms2analyses = {}

filename = sys.argv[1]
pos = "NOUN" if "noun" in filename else "VERB" if "verb" in filename else ""

with open(filename) as f:
    for line in f:
        line = line.strip()
        form, lemma, analysis = line.split(",")
        if form not in forms2analyses:
            forms2analyses[form] = []
        forms2analyses[form].append(pos + " " + " ".join(analysis.split(":")))
        #result = " ".join(form.lower()) + "\t" + pos # + " ".join(lemma)
        #for feature in analysis.split(":"):
        #    k, v = feature.split("=")
        #    result += v.upper() + " "
        #print(result.strip())


for form, _as in forms2analyses.items():
    print(" ".join(form.lower()) + "\t" + " ; ".join(_as))
