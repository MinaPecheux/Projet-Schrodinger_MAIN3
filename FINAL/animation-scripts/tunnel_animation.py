"""
Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

from math import exp
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

# NUMERIC METHODS FUNCTION -------------------------------------------
def euler_imp(y, H, n, delta_t):
    # calculation of new vector
    y = np.dot(np.linalg.inv(np.eye(n) + 1j * delta_t * H), y)
    # normalization of the vector
    y /= np.linalg.norm(y)
    return y
# --------------------------------------------------------------------

# GENERAL VARIABLES DECLARATION --------------------------------------
x_min = -50.
x_max = 50.
delta_x = 0.2
x0 = -10.
sigma = 1.5
delta_t = 0.4       # time difference between two steps

# we make the space discrete
x_values = np.arange(x_min, x_max, delta_x)

# number of subdivisions
n = len(x_values)

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure(figsize=(8, 6), dpi=150)
ax = plt.axes(xlim=(x_min, x_max), ylim=(0, 0.075))
line, = ax.plot([], [], lw=2, color='blue')

# declaration of main matrices
laplacian = -1 / (2 * delta_x**2) * (-2*np.eye(n) + np.diag(np.ones(n - 1), -1) + np.diag(np.ones(n - 1), 1))
V = np.zeros((n, n))                                               # null potential
potential = 0.3
potential_lim = [-2., 2.]
V2 = np.diag([potential if potential_lim[0] <= x_values[i] <= potential_lim[1] else 0.0 for i in range(n)])                             # potential barrier
# here you choose which potential you add:
H = laplacian + V2
# ----------------------------------------------------------------

# INITIALIZATION -----------------------------------------------------
# graph preparation: potential representation
ax.axvspan(xmin=potential_lim[0], xmax=potential_lim[1], ymin=0, ymax=1, color='red', alpha=0.5)

# declaration of initial wave function
k = -2.
psi = [exp(-(x - x0) ** 2 / (2*sigma ** 2))*np.exp(-1j * k * x) for x in x_values]

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,


# COMPUTATION + GRAPHIC REPRESENTATION ---------------------------------
# use EULER IMPLICIT method to compute the wave function movement
# animation function.  This is called sequentially
def animate(i):
    global psi
    psi = euler_imp(psi, H, n, delta_t)
    y_values = [np.absolute(v) ** 2 for v in psi]
    line.set_data(x_values, y_values)
    return line,
# ----------------------------------------------------------------

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.title('Tunnel effect (with Euler Implicit method), potential = %.1f' % potential)
plt.xlabel('Horizontal position')
plt.ylabel('Wave function')
ax.set_yticklabels([])
ax.set_xticklabels([])

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('basic_animation.mp4', fps=25, extra_args=['-vcodec', 'libx264'])

plt.show()
