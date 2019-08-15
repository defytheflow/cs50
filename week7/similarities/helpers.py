from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    a = a.split("\n")
    b = b.split("\n")
    res = list(set(a) & set(b))
    return res


def sentences(a, b):
    """Return sentences in both a and b"""
    a = set(sent_tokenize(a))
    b = set(sent_tokenize(b))
    return list(a & b)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    def spl(seq, n):
        res = []
        for i in range(len(seq)):
            if len(seq) - i < n:
                break
            sub = seq[i:i+n]
            res.append(sub)
        return res

    if n == 1:
        a, b = set(a), set(b)
        res = list(a & b)
    else:
        a = spl(a, n)
        b = spl(b, n)
        res = list(set(a) & set(b))
    return res
