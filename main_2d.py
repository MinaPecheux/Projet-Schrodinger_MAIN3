"""
File : main_2d.py
[MAIN3 - Schrodinger] Feb. - June 2017
A. Khizar, R. Ndiaye, V. Nicol, M. Pecheux
Referent: F. Aviat

Main file that represents the wave functions in 2D using the TISE.
"""

# useful imports
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


# general variables
x_min = -3
x_max = 3
lx = x_max - x_min
y_min = -3
y_max = 3
ly = y_max - y_min
n = 5     # number of subdivisions of the space
delta_x = lx / n
delta_y = ly / n
h = 6.64E-34

# we make the space discrete
x_values = np.arange(x_min, x_max, delta_x)
y_values = np.arange(y_min, y_max, delta_y)
X, Y = np.meshgrid(x_values, y_values)

# declaration of main matrices
laplacian_x = - 1 / delta_x**2 * (-2*np.eye(n*n) + np.diag(np.ones(n*n - 1), -1) + np.diag(np.ones(n*n - 1), 1))
laplacian_y = - 1 / delta_y**2 * (-2*np.eye(n*n) + np.diag(np.ones(n*n - 3), 3) + np.diag(np.ones(n*n - 3), -3))
laplacian = 1/2 * (laplacian_x + laplacian_y)
V0 = np.zeros((n*n, n*n))                                                # null potential
#V1 = np.asarray([x ** 2 for x in x_values])                     # harmonic potential
#V2 = np.asarray([abs(round(sin(3*x))) for x in x_values])       # rectangular potential
# here you choose which potential you add:
H = laplacian + V0
# we get the eigen vectors of the H matrix
# to get the eigen functions of the H operator
eigen_values, eigen_vectors = np.linalg.eigh(H)

# we create the figures
fig1, fig2 = plt.figure(1), plt.figure(2)
# we set them for 3d representation
ax1, ax2 = fig1.gca(projection='3d'), fig2.gca(projection='3d')

# orbitals that we want to compute
energy = 2
nx, ny = 2, 2

# analytic solution representation: psi^2 = presence probability
Z = (2/sqrt(lx*ly) * np.multiply(np.sin(nx * np.pi * X/lx), np.sin(ny * np.pi * Y/ly))) ** 2

# we plot the result against the x values
ax1.plot_surface(X, Y, Z, linewidth=0, antialiased=True)

# experimental solution representation: psi^2 = presence probability
psi = list(eigen_vectors[:, energy - 1])
Z = []
for i in range(n):
    Z.append([v ** 2 for v in psi[i*n:(i+1)*n]])

ax2.plot_surface(X, Y, Z, linewidth=0, antialiased=True)

plt.show()
