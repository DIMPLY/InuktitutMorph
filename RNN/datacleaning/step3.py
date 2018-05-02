"""
With the list of words vs starting positions pairs stored in "pre" half manually, this file is then used to produce the 0-1 chain, with '1' denoting the start of a new morpheme and "0" denoting not the start.
The produced words vs 0-1 chains pairs are stored in "pre2".
"""

import re,sys
if sys.argv[1]=="train":
    preffix="train-"
else:
    preffix="devel-"

#f = open(preffix+"pre","r")
#f2=open(preffix+"pre2","w")
f = open(preffix+"data","r")
f2=open(preffix+"data2","w")
for l in f:
    try:
        word, splitPos = l.strip().split('\t')
    except:
        print(l)
    splitPos = re.compile(r"\s+\+\s+").split(splitPos.strip())
    for posList in splitPos:
        posList = posList.split()
        outStr = ['0']*len(word)
        for pos in posList:
            try:
                p,t = pos.split('_')
            except:
                print(pos)
            try:
                outStr[int(p)]=t
            except:
                print(word, posList)
        f2.write(word+"\t"+"".join(outStr)+"\n")

