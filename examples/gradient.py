import numpy as np
import kurapy as kp

np.random.seed(0)
L = 20  # lattice size
N = L ** 2  # number of oscillators
alpha = 0.5  # phase shift

lattice = kp.Lattice(L)
lattice.set_distances('cartesian')

K = kp.coupling.cosine(lattice)
control = np.zeros((L, L))
control[13, 13] = control[13, 14] = control[14, 13] = control[14, 14] = 1
model = kp.Model(np.zeros(N), K, shift=alpha, control=control)

t = np.arange(400)  # time
phi0 = 2 * np.pi * np.random.rand(N)  # initial condition
phis = model.evolve(t, phi0)

phimat = kp.analyze.shape_matrix(phis)
phimat = kp.visualize.lattice_roll(phimat, -4, 0)
kp.visualize.lattice_anim(t, phimat)

laplace = kp.analyze.curvature(phimat)
kp.visualize.curvature_anim(t, laplace)

gradx, grady = kp.analyze.gradient(phimat)
kp.visualize.gradient_frame(gradx, grady)
