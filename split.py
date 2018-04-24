import sys


#words = []
#with open(sys.argv[1]) as f:
#    for line in f:
#        words.append(line.strip())

#splits = []
#with open(sys.argv[2]) as f:
#    for line in f:
#        splits.append(line.strip().split()[1:-1])


#for w, s in zip(words, splits):
with open(sys.argv[1]) as f:
    for line in f:
        w, s = line.strip().split("\t")
        result = []
        buff = ""
        for char, _s in zip(w, s):
            if int(_s):
                if buff:
                    result.append(buff)
                buff = char
            else:
                buff += char
        if buff:
            result.append(buff)
        print(w + "\t" + " ".join(result))
