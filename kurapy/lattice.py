import numpy as np


class Lattice:
    def __init__(self, size):
        self._metrics = ['cartesian', 'euclidean']

        self.size = size
        self.N = int(size ** 2)
        x = np.arange(0, self.size)
        self.positions = np.vstack(np.meshgrid(x, x)).reshape(2, -1).T

        self.metric = None
        self.distances = None

    def set_distances(self, metric, periodic=True):
        metric = metric.lower()
        if metric in self._metrics:
            pos = self.positions / self.size
            rep_pos = np.repeat(np.expand_dims(pos, axis=0), self.N, axis=0)

            if metric == 'euclidean':
                rep_pos_norm = rep_pos - np.transpose(rep_pos, (1, 0, 2))
                dmin = np.linalg.norm(rep_pos_norm, axis=2)
                if periodic:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                dist = np.linalg.norm(rep_pos_norm + np.array([i, j]), axis=2)
                                dmin = np.minimum(dmin, dist)
                self.metric = metric
                self.distances = dmin

            elif metric == 'cartesian':
                dmin = abs(rep_pos - np.transpose(rep_pos, (1, 0, 2)))
                if periodic:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i != 0 or j != 0:
                                dist = abs(dmin + np.array([i, j]))
                                dmin = np.minimum(dmin, dist)
                self.metric = metric
                self.distances = dmin

        else:
            raise ValueError('Invalid metric. Expected one of: {}'.format(self._metrics))
