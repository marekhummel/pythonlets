# matplotlib.rcParams["toolbar"] = "None"
import matplotlib.pyplot as plt  # noqa
import numpy as np

ENTS = 20

locations = np.random.rand(ENTS, 2)

# Create a plot
fig, ax = plt.subplots()
scatter = ax.scatter(locations[:, 0], locations[:, 1])

# Remove axes and other elements
ax.set_axis_off()
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)


# Function to update the points and refresh the plot
def update_points():
    global locations
    # Move points to the right by 0.01 (adjust this value to change speed)
    locations[:, 0] += 0.01
    locations[:, 0] = np.mod(locations[:, 0], 1)  # Keep points within [0,1] bounds
    scatter.set_offsets(locations)

    fig.canvas.draw_idle()


plt.ion()
while True:
    update_points()
    fig.canvas.flush_events()
