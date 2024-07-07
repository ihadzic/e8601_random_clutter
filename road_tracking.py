#!/usr/bin/env python
import matplotlib.pyplot as plt
import random
import time
from scipy.stats import norm
import numpy as np
import argparse

class RoadTrackSim:
    def __init__(self, x_vert, y_horiz, road_width,
                 velocity, velocity_variance, measurement_variance,
                 num_particles, randomize_velocity):
        self.fig, self.ax = plt.subplots()
        self.num_particles = num_particles
        self.particle_plot, = self.ax.plot([], [], 'g.')
        self.gt_plot, = self.ax.plot([], [], 'bx')
        self.measurement_plot, = self.ax.plot([], [], 'ro')
        self.velocity = velocity
        self.velocity_variance = velocity_variance
        self.randomize_velocity = randomize_velocity
        self.measurement_variance = measurement_variance
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
        self.measurement_x = None
        self.measurement_y = None
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
        if self.randomize_velocity:
            velocity = np.random.normal(loc = self.velocity,
                                        scale = np.sqrt(self.velocity_variance))
        else:
            velocity = self.velocity
        delta_t = time - self.time
        if self.gt_y < self.y_horiz:
            self.gt_y += velocity * delta_t
            delta_x = self.gt_y - self.y_horiz
            if delta_x > 0:
                self.gt_y = self.y_horiz
                self.gt_x -= delta_x
        elif self.gt_x > 0:
            self.gt_x -= velocity * delta_t

    def apply_motion_model(self, x, y, delta_t):
        def move_up(x, y, delta_t):
            return np.random.multivariate_normal(
                    mean = [ x, y + self.velocity * delta_t],
                    cov = [
                        [ self.velocity_variance * delta_t * delta_t, 0 ],
                        [ 0, self.velocity_variance * delta_t * delta_t ]
                    ]
                )
        def move_left(x, y, delta_t):
            return np.random.multivariate_normal(
                mean = [ x - self.velocity * delta_t, y],
                cov = [
                    [ self.velocity_variance * delta_t * delta_t, 0 ],
                    [ 0, self.velocity_variance * delta_t * delta_t ]
                ]
            )

        while True:
            if x > self.x1 and y > self.y1:
                # intersection, moving in either direction
                if random.choice([True, False]):
                    x_new, y_new = move_up(x, y, delta_t)
                else:
                    x_new, y_new = move_left(x, y, delta_t)
            elif x > self.x1:
                # vertical road segment, moving up
                x_new, y_new = move_up(x, y, delta_t)
            else:
                # horizontal road segment, moving left
                x_new, y_new = move_left(x, y, delta_t)
            if self.is_on_road(x_new, y_new):
                break
        return x_new, y_new

    def move_particles(self, time):
        delta_t = time - self.time
        self.predicted_particles = [
            self.apply_motion_model(*p, delta_t) for p in self.particles
        ]

    def generate_measurement(self):
        self.measurement_x, self.measurement_y = \
            np.random.multivariate_normal(
                mean = [ self.gt_x, self.gt_y ],
                cov = [[ self.measurement_variance, 0 ],
                       [ 0, self.measurement_variance ]])

    def score_particles(self):
        particle_importance = [
            norm.pdf(np.linalg.norm([x - self.measurement_x,
                                     y - self.measurement_y]),
                     scale = self.measurement_variance) \
            for x, y in self.predicted_particles
        ]
        self.particle_importance = [
            x / sum(particle_importance) for x in particle_importance ]

    def resample(self):
        sample_indices = np.random.choice(
            np.arange(0, self.num_particles), size = self.num_particles,
            p = self.particle_importance)
        self.particles = [
            self.predicted_particles[i] for i in sample_indices
        ]

    def advance_time(self, time):
        self.time = time

    def get_time(self):
        return self.time

    def redraw(self):
        self.gt_plot.set_data(self.gt_x, self.gt_y)
        self.measurement_plot.set_data(self.measurement_x, self.measurement_y)
        self.particle_plot.set_data(
            [ x[0] for x in self.particles ],
            [ x[1] for x in self.particles ])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

def display_sleep(now):
    elapsed_wall_clock_time = time.time() - now
    sleep_time = delta_t - elapsed_wall_clock_time
    if sleep_time > 0:
        time.sleep(sleep_time)

parser = argparse.ArgumentParser(
    description = 'Simulates the fusion between the map information and GPS.'
    'The vehicle is assumed to be moving at velocity v following the road.'
    'It is assumed that the velocity is known with specified variance'
    'GPS error is modeled as zero-mean Gaussian process with specified variance'
)
parser.add_argument('--xvert', type=float, default=5,
                  help='x coordinate of the vertical road segment')
parser.add_argument('--yhoriz', type=float, default=10,
                  help='y coordinate of the horizontal road segment')
parser.add_argument('--rwidth', type=float, default=1,
                  help='road width')
parser.add_argument('--vvel', type=float, default=1,
                  help='nominal vehicle velocity')
parser.add_argument('--vvar', type=float, default=0.2,
                  help='vehicle velocioty variance')
parser.add_argument('--mvar', type=float, default=1,
                  help='measurement variance')
parser.add_argument('--npart', type=int, default=500,
                  help='number of particles to use')
parser.add_argument('--randvel', action='store_true',
                    help='randomize vehicle true velocity')
args = parser.parse_args()

road_track = RoadTrackSim(
    x_vert = args.xvert,
    y_horiz = args.yhoriz,
    road_width = args.rwidth,
    velocity = args.vvel,
    velocity_variance = args.vvar,
    measurement_variance = args.mvar,
    num_particles = args.npart,
    randomize_velocity = args.randvel)

# enter interactive mode and show the plot
plt.ion()
plt.show()

delta_t = 0.1
while True:
    now = time.time()
    if road_track.gt_x > 0:
        t = road_track.get_time() + delta_t

        # ground truth simulation
        road_track.move_vehicle(t)

        # filter simulation
        road_track.move_particles(t)
        road_track.generate_measurement()
        road_track.score_particles()
        road_track.resample()

        # common (progress time)
        road_track.advance_time(delta_t)

    # treat the eyeballs
    road_track.redraw()
    display_sleep(now)
