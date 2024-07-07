#!/usr/bin/env python
import matplotlib.pyplot as plt
import random
import time


class RoadTrackSim:
    def __init__(self, x_vert, y_horiz, road_width):
        self.fig, self.ax = plt.subplots()
        self.gt_plot, = self.ax.plot([], [], 'bx')
        self.x_vert = x_vert
        self.y_horiz = y_horiz
        self.road_width = road_width
        self.x1 = self.x_vert - self.road_width / 2
        self.x2 = self.x_vert - self.road_width / 2
        self.y1 = self.y_horiz - self.road_width / 2
        self.y2 = self.y_horiz + self.road_width / 2
        self._plot_road()
        self.fig.gca().set_aspect('equal', adjustable='box')

    def _plot_road(self):
        # road edges
        self.ax.plot([self.x1, self.x1], [0, self.y1], color='black')
        self.ax.plot([self.x2, self.x2], [0, self.y2], color='black')
        self.ax.plot([self.x1, -self.road_width], [self.y1, self.y1], color='black')
        self.ax.plot([self.x2, -self.road_width], [self.y2, self.y2], color='black')

        # fill the insides of the road
        road_vertices = [
            (self.x1, 0), (self.x1, self.y1), (-self.road_width, self.y1),
            (-self.road_width, self.y2), (self.x2, self.y2), (self.x2, 0)
        ]
        self.ax.fill(*zip(*road_vertices), color='gray', alpha=0.5)

        # set the plot limits
        self.ax.set_xlim(-self.road_width, self.x_vert + self.road_width)
        self.ax.set_ylim(0, self.y_horiz + self.road_width)
        self.ax.grid()

    def redraw(self):
        self.gt_plot.set_data(random.uniform(0, 4), random.uniform(0, 4))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

road_track = RoadTrackSim(x_vert = 5, y_horiz = 10, road_width = 2)
# set aspect ratio to equal for correct representation
plt.ion()
plt.show()

for i in range(50):
    road_track.redraw()
    time.sleep(0.5)
