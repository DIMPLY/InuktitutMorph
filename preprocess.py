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
                segment = segment.split("_")[-1]
                segment = segment.replace("+", "")
                segment = segment.replace("-", " ")
                segments.append(segment)
            _morphs.append(" ".join(segments))
        print(chars + "\t" + " + ".join(_morphs))
