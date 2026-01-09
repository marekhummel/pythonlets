# ruff: noqa N816

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Create the meshgrid for (a, b) values
a_vals = np.linspace(-10, 10, 400)
b_vals = np.linspace(-10, 10, 400)
a, b = np.meshgrid(a_vals, b_vals)


def f_joint(a, b, d=3.0, sigma=0.5, sigma_b=1.0):
    with np.errstate(divide="ignore", invalid="ignore"):
        theta = np.arctan2(a, b)
        _norm_theta = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-(theta**2) / (2 * sigma**2))
        _norm_b = (1 / (np.sqrt(2 * np.pi) * sigma_b)) * np.exp(-((b - d) ** 2) / (2 * sigma_b**2))
        jacobian = 1 / (a**2 + b**2)
        return (
            (1 / (2 * np.pi * sigma * sigma_b))
            * np.exp(-(theta**2) / (2 * sigma**2) - (b - d) ** 2 / (2 * sigma_b**2))
            * jacobian
        )


# Initial parameter values
d0 = 3.0
sigma0 = 0.5
sigma_b0 = 1.0

fig, (ax_contour, ax_fA, ax_fB) = plt.subplots(1, 3, figsize=(15, 5))
plt.subplots_adjust(bottom=0.25)

# Plot initial contour
z = f_joint(a, b, d=d0, sigma=sigma0, sigma_b=sigma_b0)
contour = ax_contour.contourf(a_vals, b_vals, z, levels=100, cmap="viridis")
ax_contour.set_title("Joint PDF $f_{A,B}(a,b)$")
ax_contour.set_xlabel("a")
ax_contour.set_ylabel("b")

# Plot f_A given b = d
theta_vals = np.arctan(a_vals / d0)
f_A = (
    (1 / (np.sqrt(2 * np.pi) * sigma0))
    * np.exp(-(theta_vals**2) / (2 * sigma0**2))
    / (a_vals**2 + d0**2)
)
ax_fA.plot(a_vals, f_A)
ax_fA.set_title(r"$f_A(a) \,|\, B = d$")
ax_fA.set_xlabel("a")

# Plot f_B
f_B = (1 / (np.sqrt(2 * np.pi) * sigma_b0)) * np.exp(-((b_vals - d0) ** 2) / (2 * sigma_b0**2))
ax_fB.plot(b_vals, f_B)
ax_fB.set_title(r"$f_B(b)$")
ax_fB.set_xlabel("b")

# Define sliders
axis_d = plt.axes([0.15, 0.1, 0.65, 0.03])
axis_sigma = plt.axes([0.15, 0.06, 0.65, 0.03])
axis_sigma_b = plt.axes([0.15, 0.02, 0.65, 0.03])

slider_d = Slider(axis_d, "d", -5.0, 5.0, valinit=d0)
slider_sigma = Slider(axis_sigma, "\u03c3 (theta)", 0.1, 2.0, valinit=sigma0)
slider_sigma_b = Slider(axis_sigma_b, "\u03c3_B", 0.1, 2.0, valinit=sigma_b0)


def update(val):
    d = slider_d.val
    sigma = slider_sigma.val
    sigma_b = slider_sigma_b.val

    ax_contour.clear()
    ax_fA.clear()
    ax_fB.clear()

    z = f_joint(a, b, d=d, sigma=sigma, sigma_b=sigma_b)
    ax_contour.contourf(a_vals, b_vals, z, levels=100, cmap="viridis")
    ax_contour.set_title("Joint PDF $f_{A,B}(a,b)$")
    ax_contour.set_xlabel("a")
    ax_contour.set_ylabel("b")

    theta_vals = np.arctan(a_vals / d)
    f_A = (
        (1 / (np.sqrt(2 * np.pi) * sigma))
        * np.exp(-(theta_vals**2) / (2 * sigma**2))
        / (a_vals**2 + d**2)
    )
    ax_fA.plot(a_vals, f_A)
    ax_fA.set_title(r"$f_A(a) \,|\, B = d$")
    ax_fA.set_xlabel("a")

    f_B = (1 / (np.sqrt(2 * np.pi) * sigma_b)) * np.exp(-((b_vals - d) ** 2) / (2 * sigma_b**2))
    ax_fB.plot(b_vals, f_B)
    ax_fB.set_title(r"$f_B(b)$")
    ax_fB.set_xlabel("b")

    fig.canvas.draw_idle()


slider_d.on_changed(update)
slider_sigma.on_changed(update)
slider_sigma_b.on_changed(update)

plt.show()
