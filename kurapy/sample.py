import numpy as np
import scipy.stats as stats


def cauchy(centre=0, spread=1, size=1):
    x = stats.cauchy.rvs(loc=centre, scale=spread, size=size)
    return x


def gaussian(centre=0, spread=1, size=1):
    x = np.random.normal(centre, spread, size)
    return x


def gaussian_trunc(lim=(-1, 1), centre=0, spread=1, size=1):
    if spread == 0:
        x = centre * np.ones(size)
    else:
        a = (lim[0] - centre) / spread
        b = (lim[1] - centre) / spread
        g = stats.truncnorm(a, b, loc=centre, scale=spread)
        x = g.rvs(size)
    return x
