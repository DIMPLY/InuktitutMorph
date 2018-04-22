"""
Transform the original German word-morphemes list to contain the startingn position of each morphemes.
For morphemes that are not appearing character by character in the word, predictions are applied.
If there're continuous morphemes of the above described situation, only the first one is predicted and the following ones are using "continuous" to hold the place for their starging position.
The results are in file "temp-orig", and then manual morphorlogy analysis for the lines with "continuous" are applied with results stored in the file "temp".
The referrences and irregular formats in "temp" are then eliminated and the result stored in "pre".
"""

# python3 xxx.py train
# python3 xxx.py dev

import sys 

with open("rnn-"+sys.argv[1]+".labels.ger") as f:
    for line in f:
        line = line.strip()
        word, morph = line.split("\t")
        morphs = morph.split(", ")
        _morphs = []
        print(word, end="\t")
        for m in morphs:
            segments = []
            sstart=0
            lastIsFound=True
            for segment in m.split():
                #if not segment=='$$':
                pos=word.find(segment,sstart)
                if pos==-1:
                    if not lastIsFound:
                        print('continuous', end=" ")
                    else:
                        print(sstart, end=" ")
                    lastIsFound=False
                    sstart+=1
                else:
                    lastIsFound=True
                    sstart=pos+len(segment)
                    print(pos, end=" ")
                segments.append(segment)
            print(" + ", end="")
            _morphs.append(" ".join(segments))
        print("\t" + " + ".join(_morphs))
