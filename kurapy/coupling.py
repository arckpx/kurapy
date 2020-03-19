import numpy as np


def constant(lattice):
    K = np.ones((lattice.N, lattice.N))
    np.fill_diagonal(K, 0)
    return K


def neighbour(lattice):
    # only couples to immediate neighbours
    metrics = ['cartesian', 'euclidean']
    thres = 1.01 / lattice.size
    K = np.zeros((lattice.N, lattice.N))
    if lattice.metric == 'cartesian':
        distances = np.sum(lattice.distances, axis=-1)
    elif lattice.metric == 'euclidean':
        distances = lattice.distances
    else:
        raise TypeError('Lattice metric mismatch. Expected one of: {}'.format(metrics))
    K[distances < thres] = 1
    np.fill_diagonal(K, 0)
    return K


def cosine(lattice, n=1):
    metric = 'cartesian'
    if lattice.metric == metric:
        gx = np.cos(2 * np.pi * n * lattice.distances[:, :, 0])
        gy = np.cos(2 * np.pi * n * lattice.distances[:, :, 1])
        K = gx + gy
        np.fill_diagonal(K, 0)
        return K
    else:
        raise TypeError('Lattice metric mismatch. Expected: {}'.format(metric))


def cosine2(lattice, n=1):
    metric = 'cartesian'
    if lattice.metric == metric:
        gx = 0.5 * (np.cos(2 * np.pi * n * lattice.distances[:, :, 0]) + np.cos(2 * np.pi * (n + 1) * lattice.distances[:, :, 0]))
        gy = 0.5 * (np.cos(2 * np.pi * n * lattice.distances[:, :, 1]) + np.cos(2 * np.pi * (n + 1) * lattice.distances[:, :, 1]))
        K = gx + gy
        np.fill_diagonal(K, 0)
        return K
    else:
        raise TypeError('Lattice metric mismatch. Expected: {}'.format(metric))
