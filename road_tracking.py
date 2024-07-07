#!/usr/bin/env python
import matplotlib.pyplot as plt
import random
import time

def plot_road(ax, x_vert = 10, y_horiz = 10, road_width = 1):
    x1, x2 = x_vert - road_width / 2, x_vert + road_width / 2
    y1, y2 = y_horiz - road_width / 2, y_horiz + road_width / 2

    # road edges
    ax.plot([x1, x1], [0, y1], color='black')
    ax.plot([x2, x2], [0, y2], color='black')
    ax.plot([x1, -road_width], [y1, y1], color='black')
    ax.plot([x2, -road_width], [y2, y2], color='black')

    # fill the insides of the road
    road_vertices = [
        (x1, 0), (x1, y1), (-road_width, y1),
        (-road_width, y2), (x2, y2), (x2, 0)
    ]
    ax.fill(*zip(*road_vertices), color='gray', alpha=0.5)

    # set the plot limits
    ax.set_xlim(-road_width, x_vert + road_width)
    ax.set_ylim(0, y_horiz + road_width)
    ax.grid()

def redraw(fig, gt_plot):
    gt_plot.set_data(random.uniform(0, 4), random.uniform(0, 4))
    fig.canvas.draw()
    fig.canvas.flush_events()

fig, ax = plt.subplots()
plot_road(ax, x_vert=5, y_horiz=10, road_width=2)
gt_plot, = ax.plot([], [], 'bx')

# set aspect ratio to equal for correct representation
fig.gca().set_aspect('equal', adjustable='box')
plt.ion()
plt.show()

for i in range(50):
    redraw(fig, gt_plot)
    time.sleep(0.5)

