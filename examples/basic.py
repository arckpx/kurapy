import numpy as np
import kurapy as kp

np.random.seed(0)
L = 5  # lattice size
N = L ** 2  # number of oscillators

lattice = kp.Lattice(L)
lattice.set_distances('cartesian')

w = kp.sample.cauchy(spread=0.3, size=N)
K = kp.coupling.constant(lattice)
model = kp.Model(w, K)

t = np.arange(0, 200, 0.1)  # time
phi0 = 2 * np.pi * np.random.rand(N)  # initial condition
phis = model.evolve(t, phi0)
R, PSI = kp.analyze.global_op(phis)
kp.visualize.polar_anim(t, phis, R, PSI)
