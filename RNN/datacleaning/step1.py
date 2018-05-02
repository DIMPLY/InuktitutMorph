import sys,re
dataset = sys.argv[1]
o=open("../../data/MorphoChallenge/goldstd_"+dataset+"set.labels.ger").read().splitlines()
p=open("rnn-"+dataset+".labels.ger").read().splitlines()
o = [l.split('\t')[1] for l in o]
w = [l.split('\t')[0] for l in p]
p = [l.split('\t')[1] for l in p]
def mapMorph(orig):
    if re.compile(r'[a-z]+').fullmatch(orig):
        return '1'
    elif re.compile(r'[a-z]+_[A-Z]').fullmatch(orig):
        return '2'
    elif re.compile(r'\+[A-Z1-3]+(?:-[a-z]+)?').fullmatch(orig):
        return '3'
    else:
        return orig
os = [[[mapMorph(m) for m in x.strip().split()] for x in l.split(',')] for l in o]
fw = open('final-pre-'+dataset,'w')
for ns, word, mor in zip(os,w,p):
    mor = [m.strip().split() for m in mor.split(',')]
    fw.write(word+'\t')
    allMorSplits = []
    for morphList, numList in zip(mor,ns):
        combinedList = []
        for m,n in zip(morphList, numList):
            combinedList.append(m+'_'+n)
        combined = " ".join(combinedList)
        allMorSplits.append(combined)
    fw.write(','.join(allMorSplits)+'\n')
