import numpy as np


def relevance(likes: int, comments: int) -> float:
    return _consume(likes, comments)


def _consume(l: int, c: int) -> float:
    l += 1  # not zero
    c += 1
    alphal = 0.32
    alphac = 0.18
    delta = 0.98
    nl = np.log(l)/np.log(7)
    nc = np.log(c)/np.log(10)
    v = alphal * nl + alphac * nc
    v *= delta
    v += 0.99 - delta
    if v > 1.0:
        v = 0.99
    return v
