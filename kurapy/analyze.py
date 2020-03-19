import numpy as np
import scipy.ndimage as nd
import cv2


def shape_matrix(phi):
    shape = phi.shape
    dd = int(np.sqrt(shape[-1]))
    phimat = phi.reshape((shape[0], dd, dd)).transpose((0, 2, 1))
    return phimat


def shape_linear(phimat):
    shape = phimat.shape
    phi = phimat.transpose((0, 2, 1)).reshape((shape[0], shape[1] * shape[2]))
    return phi


def global_op(phi):
    # Global Order Parameter
    z = np.sum(np.exp(1j * phi), axis=1) / len(phi[0])
    R = np.abs(z)
    PSI = np.angle(z) % (2 * np.pi)
    return R, PSI


def local_op(phimat):
    cmat = np.exp(1j * phimat)
    push_u = np.roll(cmat, -1, axis=1)
    push_d = np.roll(cmat, 1, axis=1)
    push_l = np.roll(cmat, -1, axis=2)
    push_r = np.roll(cmat, 1, axis=2)

    z = np.mean([cmat, push_u, push_d, push_l, push_r], axis=0)
    R = np.abs(z)
    PSI = np.angle(z) % (2 * np.pi)
    return R, PSI


def curvature(phimat):
    phimat_curv = np.copy(phimat)

    laplace = np.zeros(np.shape(phimat_curv))
    for ax in [1, 2]:
        push_b = np.roll(phimat_curv, -1, axis=ax)  # up/left
        push_f = np.roll(phimat_curv, 1, axis=ax)  # down/right
        pushes = [push_b, push_f]

        dl = np.zeros(np.shape(phimat_curv))
        for push in pushes:
            pp = push - phimat_curv
            dphi = np.array([pp - 2 * np.pi, pp, pp + 2 * np.pi])
            dmin = np.amin(np.abs(dphi), axis=0)

            c1 = np.around(np.abs(dphi), decimals=4)
            c2 = np.around(dmin, decimals=4)
            dphi[c1 != c2] = 0
            dl += np.sum(dphi, axis=0)
        laplace += np.abs(dl)

    return laplace / (4 * np.pi)


def gradient(phimat):
    pc = np.copy(phimat)

    # Control exclusion
    # if control_exclusion is not None:
    #     cs = control_exclusion['cs']
    #     row_i = control_exclusion['cp'][0]
    #     row_f = control_exclusion['cp'][1]
    #     col = control_exclusion['cp'][2]
    #     pc[:, row_i:row_f + 1, col] = (pc[:, row_i:row_f + 1, col] - cs * np.pi) % (2 * np.pi)

    # Velocity field
    vx = (np.roll(pc, 1, axis=-1) - np.roll(pc, -1, axis=-1))
    vy = (np.roll(pc, 1, axis=-2) - np.roll(pc, -1, axis=-2))
    vx[vx > np.pi] -= 2 * np.pi
    vx[vx < -np.pi] += 2 * np.pi
    vy[vy > np.pi] -= 2 * np.pi
    vy[vy < -np.pi] += 2 * np.pi
    vx /= 2  # divide by length 2h
    vy /= 2  # divide by length 2h

    # Core exclusion
    laplace = curvature(pc)  # control_exclusion already accounted for
    binimg = (laplace > 0.05)
    binimg.dtype = np.uint8
    kernel = np.ones((3, 3))
    for i in range(len(binimg)):
        morphed = cv2.morphologyEx(binimg[i], cv2.MORPH_CLOSE, kernel)
        morphed.dtype = np.bool
        vx[i][morphed] = 0
        vy[i][morphed] = 0

    return vx, vy


def spiral_centroid(laplace, init_pos=(0, 0)):
    # The centroid must not be cut
    binimg = (laplace > 0.05)
    binimg.dtype = np.uint8
    yd, xd = np.where(binimg[0])
    core_dist = (init_pos[0] - xd) ** 2 + (init_pos[1] - yd) ** 2
    mask = (min(core_dist) == core_dist)
    pos = [xd[mask][0], yd[mask][0]]

    radius = np.zeros(len(binimg))
    centroid = np.zeros((len(binimg), 2))
    kernel = np.ones((3, 3))
    for i in range(len(binimg)):
        morphed = cv2.dilate(binimg[i], kernel, iterations=1)
        morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE, kernel)
        cores, num_spots = nd.label(morphed, structure=kernel)
        value = cores[pos[1], pos[0]]
        yc, xc = np.where(cores == value)
        xcm, ycm = np.mean(xc), np.mean(yc)

        radius[i] = np.sqrt(len(xc) / np.pi)
        centroid[i] = [xcm, ycm]
        pos = [int(xcm), int(ycm)]

    return radius, centroid
