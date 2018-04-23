import sys


forms2analyses = {}

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        form, lemma, analysis = line.split(",")
        if form not in forms2analyses:
            forms2analyses[form] = []
        forms2analyses[form].append(" ".join(lemma) + " " + " ".join(analysis.split(":")))
#        result = " ".join(form.lower()) + "\t"  # + " ".join(lemma)
#        for feature in analysis.split(":"):
#            k, v = feature.split("=")
#            result += v.upper() + " "
#        print(result.strip())


for form, _as in forms2analyses.items():
    print(" ".join(form.lower()) + "\t" + " ; ".join(_as))
