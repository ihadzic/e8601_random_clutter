#!/usr/bin/env python
import matplotlib.pyplot as plt

def plot_road(x_vert, y_horiz, road_width):
    x1, x2 = x_vert - road_width / 2, x_vert + road_width / 2
    y1, y2 = y_horiz - road_width / 2, y_horiz + road_width / 2

    # road edges
    plt.plot([x1, x1], [0, y1], color='black')
    plt.plot([x2, x2], [0, y2], color='black')
    plt.plot([x1, -road_width], [y1, y1], color='black')
    plt.plot([x2, -road_width], [y2, y2], color='black')

    # fill the insides of the road
    road_vertices = [
        (x1, 0), (x1, y1), (-road_width, y1),
        (-road_width, y2), (x2, y2), (x2, 0)
    ]
    plt.fill(*zip(*road_vertices), color='gray', alpha=0.5)

    # set the plot limits
    plt.xlim(-road_width, x_vert + road_width)
    plt.ylim(0, y_horiz + road_width)
    plt.grid()

    # set aspect ratio to equal for correct representation
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

plot_road(x_vert=5, y_horiz=10, road_width=2)
