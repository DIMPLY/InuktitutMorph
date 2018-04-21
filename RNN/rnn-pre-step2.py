"""
With the list of words vs starting positions pairs stored in "pre" half manually, this file is then used to produce the 0-1 chain, with '1' denoting the start of a new morpheme and "0" denoting not the start.
The produced words vs 0-1 chains pairs are stored in "pre2".
"""

import re
f = open("pre","r")
f2=open("pre2","w")
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
                outStr[int(pos)]='1'
            except:
                print(word, posList)
        f2.write(word+"\t"+"".join(outStr)+"\n")

