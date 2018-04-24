import sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        word, morph = line.split("\t")
        chars = " ".join(word)
        morphs = morph.split(", ")
        _morphs = []
        for m in morphs:
            segments = []
            for segment in m.split():
                if "_" in segment:
                    segment = segment.split("_")[0]
                #segment = segment.split("_")[-1]
                #segment = segment.replace("+", "")
                #segment = segment.replace("-", " ")
                segments.append(segment)
            _morphs.append(" ".join(segments))
            print(chars + "\t" + " ".join(segments)) #" + ".join(_morphs))
            break
