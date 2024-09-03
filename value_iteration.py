#!/usr/bin/env python
import argparse
import numpy as np

parser = argparse.ArgumentParser(
    description = "Runs value-iteration algorithm on a grid of "
    "specified size assuming the motion model that makes the robot "
    "move in the specified direction with probability 1 - n * p "
    "where p is the probability of skidding or slipping and moving in "
    "one of other possible directions.")
parser.add_argument('--gamma', '-g', type=float, default = 0.9,
                    help='discount factor gamma')
parser.add_argument('--xgrid', '-x', type=int, default = 4,
                    help='grid size in x-dimension')
parser.add_argument('--ygrid', '-y', type=int, default = 4,
                    help='grid size in y-dimension')
parser.add_argument('--probslip' '-p', type=float, default = 0.1,
                    help='slip/skid probability')
parser.add_argument('--movecost', '-m', type=float, default = 1,
                    help='cost of moving')
parser.add_argument('--epsilon', '-e', type=float, default = 1e-3,
                    help='epsilon for convergence criteria')
args = parser.parse_args()

terminal_states = [
    { 'x': 0, 'y': 1, 'value': -100 },
    { 'x': 0, 'y': 0, 'value': 50 },
    { 'x': 1, 'y': 2, 'value': -100 }
]

def terminal_state(x, y):
    for ts in terminal_states:
        if x == ts['x'] and y == ts['y']:
            return ts['value']
    return None

def init_values():
    values = np.zeros((args.xgrid, args.ygrid))
    for x in range(args.xgrid):
        for y in range(args.ygrid):
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
    if x+1 < args.xgrid:
        neighbors.append((x+1, y))
    # top neighbor
    if y-1 >=0:
        neighbors.append((x, y-1))
    if y+1 < args.ygrid:
        neighbors.append((x, y+1))
    return neighbors

def get_motion_distro(neighbors):
    move_prob = 1 - (len(neighbors) - 1) * args.probslip_p
    distro = []
    for n in range(len(neighbors)):
        d = [ args.probslip_p ] * len(neighbors)
        d[n] = move_prob
        distro.append(d)
    return distro

def iterate(values):
    new_values = init_values()
    for x in range(args.xgrid):
        for y in range(args.ygrid):
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
                        (expected_V - args.movecost)
                    )
                new_values[x, y] = args.gamma * max(motion_candidate_values)
    return new_values

iteration_count=0
values = init_values()
print("Init")
print(values)
print("")
delta = float("inf")
while delta > args.epsilon:
    iteration_count+=1
    print("Iteration {}".format(iteration_count))
    new_values = iterate(values)
    delta = np.max(np.abs(new_values - values))
    values = new_values
    print(np.round(values, 2))
    print("")
