import sys

with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        word, morph = line.split("\t")
        chars = " ".join(word)
        morphs = morph.split(", ")
        for m in morphs:
            segments = []
            for segment in m.split():
                segment = segment.split("_")[-1]
                segments.append(segment)
            print(chars + "\t" + " ".join(segments))
