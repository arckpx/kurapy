# Kurapy

Python package for simulation of Kuramoto model in a fully-filled square lacttice.

## Installation

Use the package manager pip to install Kurapy:
```
pip install kurapy
```


## Usage

Construct a lattice and obtain the coupling matrix:
```
import kurapy as kp

size = 15
lattice = kp.Lattice(size)
lattice.set_distances('cartesian')
coupling_matrix = kp.coupling.cosine(lattice)
```
Define the model and run the simulation:
```
natural_frequencies = np.zeroes(N)
model = kp.Model(natural_frequencies, coupling_matrix)

t = np.arange(200)  # time
phi0 = 2 * np.pi * np.random.rand(N)  # initial condition
phis = model.evolve(t, phi0)
```
Visualize with an animated plot:
```
phimat = kp.analyze.shape_matrix(phis)
kp.visualize.lattice_anim(t, phimat)
```
Refer to [examples](examples/) for more details:
1. basic.py
2. curvature.py
3. gradient.py

The following are some example outputs:

![alt text](https://github.com/arckpx/kurapy/blob/master/examples/output.png "Example Output")

## Built With

* [NumPy](http://www.numpy.org/)
* [SciPy](https://www.scipy.org/)
* [Matplotlib](https://matplotlib.org/)
* [OpenCV-Python](https://opencv-python-tutroals.readthedocs.io/en/latest/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
