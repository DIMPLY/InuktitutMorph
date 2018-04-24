import sys

seen = set()
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        word = "".join(line.split())
        if word in seen:
            continue
        seen.add(word)
        print(line)
