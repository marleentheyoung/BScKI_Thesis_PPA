import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import benchmark
import benchmark_functions as benchmarks

def helperfunc(x, y, a):
    return a[0] + np.sum([a[i] * x**(i-1) for i in range(1, 4)]) + \
            np.sum([a[i] * y**(i-4) for i in range(4, 7)]) + \
                a[7] * x*y + a[8]* x**2*y + a[9] * y**2*x

def poly_second_degree(x, y, a):
    return -1 * (a[0] + np.sum([a[i] * x**(i-1) for i in range(1, 3)]) + \
            np.sum([a[i] * y**(i-3) for i in range(3, 5)]) + a[5] * x*y)


def f(x, y):
    print(np.sin(np.sqrt(x ** 2 + y ** 2)))
    return np.sin(np.sqrt(x ** 2 + y ** 2))

def p(x):
    return x**4 - 4*x**2 + 3*x



# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='binary')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')


# # X = np.linspace(-3, 3, 50, endpoint=True)
# # F = func(X)
# # print(F)
# # plt.plot(X,F)

# plt.show()

# Create figure and add axis
fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111, projection='3d')

# Remove gray panes and axis grid
ax.xaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('white')
ax.yaxis.pane.fill = False
ax.yaxis.pane.set_edgecolor('white')
ax.zaxis.pane.fill = False
ax.zaxis.pane.set_edgecolor('white')
ax.grid(False)
# Remove z-axis
ax.w_zaxis.line.set_lw(0.)
ax.set_zticks([])

# Create meshgrid
X, Y = np.meshgrid(np.linspace(0, 2, len(afm_data)), np.linspace(0, 2, len(afm_data)))

# Plot surface
plot = ax.plot_surface(X=X, Y=Y, Z=Z, cmap='YlGnBu_r', vmin=0, vmax=200)

plt.show()


