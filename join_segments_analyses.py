import sys


w2a = {}
# read word2analysis
with open(sys.argv[2]) as f:
    for line in f:
        line = line.strip()
        w, a = line.split("\t")
        if w not in w2a:
            w2a[w] = []
        w2a[w].append(a)


w2s = {}
# read word2segments
with  open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        w, s = line.split("\t")
        if w not in w2s:
            w2s[w] = []
        w2s[w].append(s)


assert len(w2a.keys()) == len(w2s.keys())


for word in w2a.keys():
    print(w2s[word][0] + "\t" + w2a[word][0])
