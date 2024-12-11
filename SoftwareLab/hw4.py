import operator
import lib601.util as util
# python 2.6.6
class DDist:
    def __init__(self, dictionary):
        self.d = dictionary

    def dictCopy(self):
        return self.d.copy()

    def prob(self, elt):
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0

    def support(self):
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add, [util.prettyString(k)+": "+util.prettyString(p)+", " for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__

def incrDictEntry(d, k, v):
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v

class MixtureDist:
    def __init__(self, d1, d2, p):
        self.d1 = d1.dictCopy()
        self.d2 = d2.dictCopy()
        self.p = float(p)

    def prob(self, elt):
        d1_prob = self.d1[elt] if elt in self.d1 else 0
        d2_prob = self.d2[elt] if elt in self.d2 else 0
        return d1_prob * self.p + d2_prob * (1 - self.p)

    def support(self):
        list1 = [k for k in self.d1.keys() if self.prob(k) > 0]
        list2 = [k for k in self.d2.keys() if self.prob(k) > 0]
        return list(set(list1 + list2))

    def __str__(self):
        elts = self.support()
        result = 'MixtureDist({'+', '.join('%s : %s' % (str(x), str(self.prob(x))) for x in elts)+'})'
        return result

    __repr__ = __str__

def squareDist(lo, hi, loLimit=None, hiLimit=None):
    dist1, p, loLimit, hiLimit = {}, 1.0 / (hi - lo), lo - 1 if loLimit is None else loLimit, hi + 1 if hiLimit is None else hiLimit
    if loLimit >= hi: dist1[loLimit] = 1
    if hiLimit <= lo: dist1[hiLimit] = 1
    if loLimit < hi and hiLimit > lo:
        start, end = max(lo, loLimit), min(hi, hiLimit)
        for i in range(start, end): incrDictEntry(dist1, i, p)
        if end < hi: dist1[end] = (hi - end) * p
    return DDist(dist1)

def triangleDist(peak, halfWidth, loLimit=None, hiLimit=None):
    dist1, p, lo, hi = {}, 1.0 / (halfWidth)**2, peak - halfWidth + 1, peak + halfWidth
    loLimit, hiLimit = lo - 1 if loLimit is None else loLimit, hi + 1 if hiLimit is None else hiLimit
    if loLimit >= hi: dist1[loLimit] = 1
    if hiLimit <= lo: dist1[hiLimit] = 1
    for i in range(lo, hi): incrDictEntry(dist1, i, abs(abs(i - peak) - halfWidth) * p)
    if lo <= loLimit < hi:
        dist1[loLimit] = sum(dist1.pop(j, 0) for j in range(lo, loLimit))
    if lo < hiLimit <= hi:
        dist1[hiLimit] = sum(dist1.pop(k, 0) for k in range(hiLimit, hi))
    return DDist(dist1)

import lib601.sig as sig

class IntDistSignal(sig.Signal):
    def __init__(self, d):
        self.dist = d
    def sample(self, n):
        return self.dist.prob(n)
def plotIntDist(d, n):
    IntDistSignal(d).plot(end = n, yOrigin = 0)

print 'step1\n'
print squareDist(2, 4)
print squareDist(2, 5)
print squareDist(2, 5, 0, 10)
print squareDist(2, 5, 6, 10)
print '-----\n'
print 'step2\n'
print triangleDist(5, 1)
print triangleDist(5, 2)
print triangleDist(5, 3)
print triangleDist(5, 3, 0, 10)
print '-----\n'
print 'step3\n'
print MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.5)
print MixtureDist(squareDist(2, 4), squareDist(10, 12), 0.9)
print MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5)