def precision(ygold, ypred):
    gold = set(ygold)
    pred = set(ypred)
    tp = gold.intersection(pred)
    return len(tp)/len(pred)


def recall(ygold, ypred):
    gold = set(ygold)
    pred = set(ypred)
    tp = gold.intersection(pred)
    return len(tp)/len(gold)


def fmeasure(ygold, ypred):
    gold = set(ygold)
    pred = set(ypred)
    tp = gold.intersection(pred)
    p, r = len(tp)/len(pred), len(tp)/len(gold)

    if p+r == 0:
        return 0.0
    return (2*p*r)/(p+r)


def tensor_wrapper(metric):
    return lambda x, y: metric(x[0], y[0])
