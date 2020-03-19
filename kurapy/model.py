import sys
import numpy as np


class Model:
    def __init__(self, freq, coupling, shift=0, second_order=0, noise=0, control=None):
        """
        :param freq: (N) natural oscillator frequencies
        :param coupling: (N x N) coupling matrix
        :param shift: (int) phase shift
        :param second_order: (int) second-order contribution
        :param noise: (int) Gaussian noise level
        :param control: (N x N) control strength ranging from 0 to 1
        """
        self._N = len(freq)
        self._L = int(np.sqrt(self._N))
        self._freq = freq
        self._coupling = coupling
        self._second_order = second_order
        self._shift = shift
        self._noise = noise
        self._control = control
        self._methods = ['forward_euler', 'rk4']

    def evolve(self, t, phi0, method='rk4', verbose=False):
        if method in self._methods:

            def dpdt(phi):
                return self._freq + np.sum(self._coupling * np.sin(np.subtract.outer(phi, phi) + self._shift), axis=0) / self._N + np.random.normal(0, self._noise * np.pi, size=self._N)

            def apply_control(phi):
                phimat = np.reshape(phi, (self._L, self._L))
                sites = np.argwhere(self._control != 0)
                new_phimat = phimat.copy()
                for s in sites:
                    locs = [(s[0], (s[1] - 1) % self._L),
                            (s[0], (s[1] + 1) % self._L),
                            ((s[0] - 1) % self._L, s[1]),
                            ((s[0] + 1) % self._L, s[1])]
                    ns = []
                    for i in locs:
                        if self._control[i[0], i[1]] == 0:
                            ns.append(np.exp(1j * phimat[i[0], i[1]]))
                    if not ns:
                        ns.append(0)
                    new_phimat[s[0], s[1]] = np.angle(np.mean(ns, axis=0)) + self._control[s[0], s[1]] * np.pi
                return np.reshape(new_phimat % (2 * np.pi), self._N)

            def verbosity(idx, length):
                sys.stdout.flush()
                sys.stdout.write('\rTime Step: {}/{}'.format(idx + 1, length))

            dt = t[1] - t[0]
            phis = np.zeros((len(t), len(phi0)))
            phis[0] = phi0

            if method == 'forward_euler':
                for i in range(len(phis) - 1):
                    if verbose:
                        verbosity(i, len(t))
                    k = dpdt(phis[i])
                    phis[i + 1] = (phis[i] + dt * k) % (2 * np.pi)
                    if self._control is not None:
                        phis[i + 1] = apply_control(phis[i + 1])

            elif method == 'rk4':
                for i in range(len(phis) - 1):
                    if verbose:
                        verbosity(i, len(t))
                    k1 = dpdt(phis[i])
                    k2 = dpdt(phis[i] + 0.5 * dt * k1)
                    k3 = dpdt(phis[i] + 0.5 * dt * k2)
                    k4 = dpdt(phis[i] + dt * k3)
                    phis[i + 1] = (phis[i] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)) % (2 * np.pi)
                    if self._control is not None:
                        phis[i + 1] = apply_control(phis[i + 1])

            else:
                raise ValueError('Invalid method. Expected one of: {}'.format(self._methods))

            return phis

        else:
            raise ValueError('Invalid method. Expected one of: {}'.format(self._methods))
