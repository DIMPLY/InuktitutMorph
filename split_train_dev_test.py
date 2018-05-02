import sys

if len(sys.argv) < 4:
    print('python x.py inflections_x.csv baseforms_x_train baseforms_x_dev baseforms_x_test', file=sys.stderr)
    exit(1)



infl, forms_train, forms_dev, forms_test = sys.argv[1:]

out_prefix = infl.split('/')[-1].rsplit('.', maxsplit=1)[0]


form2analyses = {}

with open(infl) as f:
    for line in f:
        line = line.strip().lower()
        _, form, _ = line.split(',')
        if form not in form2analyses:
            form2analyses[form] = []
        form2analyses[form].append(line)


for filename, _set in zip([forms_train, forms_dev, forms_test], ['train', 'dev', 'test']):
    with open(filename) as f:
        with open(out_prefix + '_' + _set + '.csv', 'w') as g:
            for line in f:
                line = line.strip().lower()
                for analysis in form2analyses[line]:
                    g.write(analysis + '\n')
