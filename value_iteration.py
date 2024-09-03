#!/usr/bin/env python

import numpy as np

gamma = 0.9
grid_size_x = 4
grid_size_y = 4
slip_skid_prob = 0.1
move_cost = 1
terminal_states = [
    { 'x': 0, 'y': 1, 'value': -100 },
    { 'x': 0, 'y': 0, 'value': 50 },
    { 'x': 1, 'y': 2, 'value': -100 }
]
epsilon = 0.001

def terminal_state(x, y):
    for ts in terminal_states:
        if x == ts['x'] and y == ts['y']:
            return ts['value']
    return None

def init_values():
    values = np.zeros((grid_size_x, grid_size_y))
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            v = terminal_state(x, y)
            if v is not None:
                values[x, y] = v
    return values

def get_neighbors(x, y):
    neighbors = []
    # left neighbor
    if x-1 >=0:
        neighbors.append((x-1, y))
    # right neighbor
    if x+1 < grid_size_x:
        neighbors.append((x+1, y))
    # top neighbor
    if y-1 >=0:
        neighbors.append((x, y-1))
    if y+1 < grid_size_y:
        neighbors.append((x, y+1))
    return neighbors

def get_motion_distro(neighbors):
    move_prob = 1 - (len(neighbors) - 1) * slip_skid_prob
    distro = []
    for n in range(len(neighbors)):
        d = [ slip_skid_prob ] * len(neighbors)
        d[n] = move_prob
        distro.append(d)
    return distro

def iterate(values):
    new_values = init_values()
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if not terminal_state(x, y):
                neighbors = get_neighbors(x, y)
                motion_distro = get_motion_distro(neighbors)
                motion_candidate_values = []
                # outer loop iterates over control options
                for i in range(len(neighbors)):
                    # inner loop calculates expected V
                    p_x_given_u = motion_distro[i]
                    expected_V = 0
                    for j in range(len(neighbors)):
                        expected_V += values[neighbors[j]] * p_x_given_u[j]
                    motion_candidate_values.append(
                        (expected_V - move_cost)
                    )
                new_values[x, y] = gamma * max(motion_candidate_values)
    return new_values

iteration_count=0
values = init_values()
print("Init")
print(values)
delta = float("inf")
while delta > epsilon:
    iteration_count+=1
    print("Iteration {}".format(iteration_count))
    new_values = iterate(values)
    print(np.round(values, 2))
    print("")
    delta = np.max(np.abs(new_values - values))
    values = new_values
