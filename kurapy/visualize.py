import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.colors as col
from matplotlib import gridspec
import sys


def coupling_plot(k0_list, Rm_list, cauchy=False):
    plt.figure(figsize=(9, 6))

    if cauchy:
        theox = np.linspace(k0_list[0], k0_list[-1], num=201)
        theoy = np.zeros(len(theox))
        for i in range(len(theox)):
            if theox[i] > 2:
                theoy[i] = np.sqrt(1 - 2 / theox[i])
        plt.plot(theox, theoy, 'r-')

    plt.plot(k0_list, Rm_list, 'kx')
    fs = 18
    plt.xlabel(r'$k_0$', fontsize=fs)
    plt.xticks(fontsize=fs)
    plt.ylabel(r'$R$', fontsize=fs)
    plt.yticks(fontsize=fs)
    plt.show()


def polar_anim(t, phi, R, PSI, rotating=False, save=False, filename='polar'):
    fig = plt.figure(figsize=(6, 7))
    gs = gridspec.GridSpec(2, 1, height_ratios=[5, 1])

    ax1 = plt.subplot(gs[0], polar=True)
    ax1.set_ylim([0, 1.2])
    ax1.set_yticks([1])
    ax1.set_yticklabels([])
    ax1.set_theta_direction(-1)
    ax1.set_theta_offset(np.pi / 2.0)

    ax2 = plt.subplot(gs[1])
    ax2.set_xlim([0, t[-1]])
    ax2.set_xlabel('t')
    ax2.set_ylim([0, 1])
    ax2.set_ylabel('R')
    ax2.grid(True)

    # Animation
    title = ax1.text(0.5, 0.8, '', bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                     transform=ax1.transAxes, ha="center")
    nodes, = ax1.plot([], [], 'bo', markersize=5, animated=True)
    avg_node, = ax1.plot([], [], 'ko', markersize=5, animated=True)
    op_plot, = ax2.plot([], [], 'k-', animated=True)
    T = []
    OP = []

    def update(i):
        if rotating:
            ref = PSI[i]
        else:
            ref = 0
        # Plot 1
        nodes.set_data((phi[i] - ref) % (2 * np.pi), 1)
        avg_node.set_data((PSI[i] - ref) % (2 * np.pi), R[i])
        # Plot 2
        T.append(t[i])
        OP.append(R[i])
        op_plot.set_data(T, OP)
        # Text
        title.set_text('t = {:.2f}'.format(t[i]))

        return nodes, avg_node, op_plot, title,

    anim = ani.FuncAnimation(fig, update, frames=len(t),
                             interval=30, blit=True, repeat=False)

    if save:
        sys.stdout.flush()
        sys.stdout.write('\rSaving...')
        Writer = ani.writers['ffmpeg']
        writer = Writer(fps=20)
        anim.save('{}.mp4'.format(filename), writer=writer)
        sys.stdout.flush()
        sys.stdout.write('\rSaved!\n')
        plt.close('all')
    else:
        plt.show()


def lattice_roll(matrix, xroll, yroll):
    matrix = np.roll(matrix, xroll, axis=2)
    matrix = np.roll(matrix, yroll, axis=1)
    return matrix


def lattice_anim(t, phimat, c='hsv', interpolation=False, save=False, filename='lattice'):
    fig, ax = plt.subplots()
    title = fig.suptitle('')

    colormap = plt.get_cmap(c)
    colormap.set_bad(color='black')
    if interpolation:
        inter = 'spline16'
    else:
        inter = 'None'
    plot = ax.matshow(phimat[0], cmap=colormap, interpolation=inter)
    ax.set_xticks([-0.5, phimat.shape[-1] - 0.5])
    ax.set_yticks([-0.5, phimat.shape[-1] - 0.5])
    ax.set_xticklabels(['$0$', '$1$'])
    ax.set_yticklabels(['$0$', '$1$'])

    plot.set_clim([0, 2 * np.pi])
    cbar = fig.colorbar(plot, ticks=[0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2 * np.pi])
    cbar.ax.set_yticklabels(['$0$', '$\pi /2$', '$\pi$', '$3\pi/2$', '$2\pi$'])

    def update(i):
        title.set_text('t = {:.2f}'.format(t[i]))
        plot.set_data(phimat[i] % (2 * np.pi))
        return [plot], title,

    anim = ani.FuncAnimation(fig, update, frames=len(t),
                             interval=30, blit=False, repeat=False)
    if save:
        sys.stdout.flush()
        sys.stdout.write('\rSaving...')
        Writer = ani.writers['ffmpeg']
        writer = Writer(fps=20)
        anim.save('{}.mp4'.format(filename), writer=writer)
        sys.stdout.flush()
        sys.stdout.write('\rSaved!\n')
        plt.close('all')
    else:
        plt.show()


def lattice_frame(matrix, frame=-1, c='hsv', interpolation=False, save=False, filename='lattice'):
    fig, ax = plt.subplots()

    colormap = plt.get_cmap(c)
    colormap.set_bad(color='black')
    if interpolation:
        inter = 'spline16'
    else:
        inter = 'None'
    plot = ax.matshow(matrix[frame], cmap=colormap, interpolation=inter)
    ax.set_xticks([-0.5, matrix.shape[-1] - 0.5])
    ax.set_yticks([-0.5, matrix.shape[-1] - 0.5])
    ax.set_xticklabels(['$0$', '$1$'])
    ax.set_yticklabels(['$0$', '$1$'])

    plot.set_clim([0, 2 * np.pi])
    cbar = fig.colorbar(plot, ticks=[0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2 * np.pi])
    cbar.ax.set_yticklabels(['$0$', '$\pi /2$', '$\pi$', '$3\pi/2$', '$2\pi$'])

    if save:
        plt.savefig(filename, bbox_inches='tight')
        plt.close('all')
    else:
        plt.show()


def curvature_anim(t, laplace, c='jet', interpolation=False, save=False, filename='curvature'):
    fig, ax = plt.subplots()
    title = fig.suptitle('')

    colormap = plt.get_cmap(c)
    colormap.set_bad(color='black')
    if interpolation:
        inter = 'spline16'
    else:
        inter = 'None'
    plot = ax.matshow(laplace[0], cmap=colormap, interpolation=inter)
    ax.set_xticks([-0.5, laplace.shape[-1] - 0.5])
    ax.set_yticks([-0.5, laplace.shape[-1] - 0.5])
    ax.set_xticklabels(['$0$', '$1$'])
    ax.set_yticklabels(['$0$', '$1$'])

    plot.set_clim([0, 1])
    cbar = fig.colorbar(plot, ticks=[0, 0.25, 0.5, 0.75, 1])
    cbar.ax.set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'])

    def update(i):
        title.set_text('t = {:.2f}'.format(t[i]))
        plot.set_data(laplace[i])
        return [plot], title,

    anim = ani.FuncAnimation(fig, update, frames=len(t),
                             interval=30, blit=False, repeat=False)
    if save:
        sys.stdout.flush()
        sys.stdout.write('\rSaving...')
        Writer = ani.writers['ffmpeg']
        writer = Writer(fps=20)
        anim.save('{}.mp4'.format(filename), writer=writer)
        sys.stdout.flush()
        sys.stdout.write('\rSaved!\n')
        plt.close('all')
    else:
        plt.show()


def curvature_frame(matrix, frame=-1, c='jet', interpolation=False, save=False, filename='curvature'):
    fig, ax = plt.subplots()

    colormap = plt.get_cmap(c)
    colormap.set_bad(color='black')
    if interpolation:
        inter = 'spline16'
    else:
        inter = 'None'
    plot = ax.matshow(matrix[frame], cmap=colormap, interpolation=inter)
    ax.set_xticks([-0.5, matrix.shape[-1] - 0.5])
    ax.set_yticks([-0.5, matrix.shape[-1] - 0.5])
    ax.set_xticklabels(['$0$', '$1$'])
    ax.set_yticklabels(['$0$', '$1$'])

    plot.set_clim([0, 1])
    cbar = fig.colorbar(plot, ticks=[0, 0.25, 0.5, 0.75, 1])
    cbar.ax.set_yticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'])

    if save:
        plt.savefig(filename, bbox_inches='tight')
        plt.close('all')
    else:
        plt.show()


# def gradient_anim(t, grad_x, grad_y, skip=1, save=False, filename='gradient'):
#     dim = grad_x.shape[-1]
#     Y, X = np.mgrid[0:1:dim * 1j, 0:1:dim * 1j]
#     U = grad_x[0]
#     V = grad_y[0]
#
#     fig, ax = plt.subplots()
#     ax.set_aspect(aspect=1)
#     title = fig.suptitle('')
#
#     si = (slice(None, None, skip), slice(None, None, skip))
#     Q = ax.quiver(X[si], Y[si], U[si], V[si],
#                   pivot='mid', color='k', units='inches',
#                   headwidth=6, headlength=6)
#     ax.set_xticks([0, 1])
#     ax.set_yticks([0, 1])
#     ax.set_xticklabels(['$0$', '$1$'])
#     ax.set_yticklabels(['$0$', '$1$'])
#
#     ax.set_xlim(0, 1)
#     ax.set_ylim(0, 1)
#
#     def update(i, Q, X, Y):
#         title.set_text('t = {:.2f}'.format(t[i]))
#         U = grad_x[i][si]
#         V = grad_y[i][si]
#         Q.set_UVC(U, V)
#         return Q, title,
#
#     anim = ani.FuncAnimation(fig, update, fargs=(Q, X, Y), frames=len(t),
#                              interval=30, blit=False, repeat=False)
#     if save:
#         sys.stdout.flush()
#         sys.stdout.write('\rSaving...')
#         Writer = ani.writers['ffmpeg']
#         writer = Writer(fps=20)
#         anim.save('{}.mp4'.format(filename), writer=writer)
#         sys.stdout.flush()
#         sys.stdout.write('\rSaved!\n')
#         plt.close('all')
#     else:
#         plt.show()


def gradient_frame(grad_x, grad_y, skip=1, frame=-1, save=False, filename='gradient'):
    dim = grad_x.shape[-1]
    Y, X = np.mgrid[0:1:dim * 1j, 0:1:dim * 1j]
    U = grad_x[frame]
    V = grad_y[frame]

    fig, ax = plt.subplots()
    ax.set_aspect(aspect=1)

    si = (slice(None, None, skip), slice(None, None, skip))
    Q = ax.quiver(X[si], Y[si], U[si], V[si],
                  pivot='mid', color='k', units='inches',
                  headwidth=6, headlength=6)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['$0$', '$1$'])
    ax.set_yticklabels(['$0$', '$1$'])

    if save:
        plt.savefig(filename, bbox_inches='tight')
        plt.close('all')
    else:
        plt.show()


def create_cmap(*args):
    """
    'r': red
    'o': orange
    'y': yellow
    'g': green
    't': turquoise
    'b': blue
    'v': violet
    'p': pink
    'w': white
    'k': black
    """
    colorlist = ['r', 'o', 'y', 'g', 't',
                 'b', 'v', 'p', 'w', 'k']
    hexlist = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#00ffff',
               '#0000ff', '#8000ff', '#ff00ff', '#ffffff', '#000000']
    display = []
    for arg in args:
        for j in range(len(colorlist)):
            if arg == colorlist[j]:
                display.append(hexlist[j])
    colormap = col.LinearSegmentedColormap.from_list(
        'anglemap', display, N=256, gamma=1)
    return colormap
