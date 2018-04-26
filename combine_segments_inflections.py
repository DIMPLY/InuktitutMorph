import sys



def replaceUmlauts(string):
    return string.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")



segments = sys.argv[1]
inflections = sys.argv[2]


state = 0
word2segm = {}
with open(segments) as f:
    for line in f:
        line = line.strip()
        if state > 2 and not line:
            if word:
                if word not in word2segm:
                    word2segm[word] = set()
                word2segm[word].add(segm)
            state = 0
            continue
        elif state == 0:
            word = line
        elif state == 2:
            segm = line

        state += 1

with open(inflections) as f:
    for line in f:
        line = line.strip()
        form, analyses = line.split("\t")
        form = replaceUmlauts("".join(form.split()))
        if form not in word2segm:
            print(f"Warning: did't find segmentation for {form}", file=sys.stderr)
            continue
        segmented = word2segm[form]
        if len(segmented) > 1:
            print(f"Warning: found multiple segmentations for {form}", file=sys.stderr)
            continue
        segmented = list(segmented)[0]
        print(f"{segmented}\t{analyses}")
