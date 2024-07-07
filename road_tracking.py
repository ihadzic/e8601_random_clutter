#!/usr/bin/env python
import matplotlib.pyplot as plt
import random
import time
import numpy as np

class RoadTrackSim:
    def __init__(self, x_vert, y_horiz, road_width, velocity, num_particles):
        self.fig, self.ax = plt.subplots()
        self.num_particles = num_particles
        self.gt_plot, = self.ax.plot([], [], 'bx')
        self.velocity = velocity
        self.x_vert = x_vert
        self.y_horiz = y_horiz
        self.road_width = road_width
        self.x1 = self.x_vert - self.road_width / 2
        self.x2 = self.x_vert + self.road_width / 2
        self.y1 = self.y_horiz - self.road_width / 2
        self.y2 = self.y_horiz + self.road_width / 2
        self.plot_road()
        self.fig.gca().set_aspect('equal', adjustable='box')
        self.time = 0
        self.gt_x = x_vert
        self.gt_y = 0
        self.init_particles(var = 1)

    def is_on_road(self, x, y):
        if x > self.x1 and x < self.x2 and y < self.y2:
            return True
        if y > self.y1 and y < self.y2 and x < self.x2:
            return True
        return False

    def init_particles(self, var):
        def get_particles(mean, cov, num):
            return [ tuple(x) for x in np.random.multivariate_normal(
                mean, cov, num) ]
        def prune_particles(particles):
            return [ p for p in particles if self.is_on_road(*p) ]
        particles = []
        while len(particles) < self.num_particles:
            particles += prune_particles(
                get_particles([self.gt_x, self.gt_y],
                              [[var, 0 ],[0, var]],
                              self.num_particles))
        self.particles = particles[0:self.num_particles]

    def plot_road(self):
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

    def move_vehicle(self, time):
        delta_t = time - self.time
        if self.gt_y < self.y_horiz:
            self.gt_y += self.velocity * delta_t
            delta_x = self.gt_y - self.y_horiz
            if delta_x > 0:
                self.gt_y = self.y_horiz
                self.gt_x -= delta_x
        elif self.gt_x > 0:
            self.gt_x -= self.velocity * delta_t

    def advance_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def redraw(self):
        self.gt_plot.set_data(self.gt_x, self.gt_y)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

def display_sleep(now):
    elapsed_wall_clock_time = time.time() - now
    sleep_time = delta_t - elapsed_wall_clock_time
    if sleep_time > 0:
        time.sleep(sleep_time)

road_track = RoadTrackSim(
    x_vert = 5,
    y_horiz = 10,
    road_width = 1,
    velocity = 1,
    num_particles = 500)
# set aspect ratio to equal for correct representation
plt.ion()
plt.show()

delta_t = 0.1
max_iter = 500
for i in range(max_iter):
    now = time.time()
    t = road_track.get_time() + delta_t
    road_track.move_vehicle(t)
    road_track.advance_time(delta_t)
    road_track.redraw()
    display_sleep(now)
