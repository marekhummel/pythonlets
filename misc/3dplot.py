import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = plt.axes(projection="3d")


def f(x, y):
    return np.sin(np.sqrt(x**2 + y**2))


x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap="viridis", edgecolor="none")
ax.set_title("surface")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
fig.savefig("out.jpg")
