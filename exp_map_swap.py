#!/usr/bin/env python
import numpy
import math
import random

def skew_sim_mat(x, y, z):
    return numpy.array([
        [0, -z, y],
        [z, 0, -x],
        [-y, x, 0]
        ])

def rodrigues(k, theta):
    return numpy.identity(3) + \
        math.sin(theta) * skew_sim_mat(*k) + \
        (1 - math.cos(theta)) * (skew_sim_mat(*k) @ skew_sim_mat(*k))

max_error = 0
for i in range(100000):

    krand = (random.random(), random.random(), random.random())
    krand /= numpy.linalg.norm(krand)
    theta = random.random()*math.pi
    k = numpy.array([krand]).transpose()
    E = rodrigues(krand, theta)

    rrand = (random.random(), random.random(), random.random())
    rrand /= numpy.linalg.norm(rrand)
    rtheta = random.random()*math.pi
    R = rodrigues(rrand, rtheta)

    RERT =R @ E @ (R.transpose())
    EXPRKTH = rodrigues((R @ k).flatten(), theta)

    ERROR = numpy.linalg.norm(RERT - EXPRKTH)
    if ERROR > 1e-8:
        print("Ooops! ERROR is {}".format(ERROR))
        exit(1)
    if ERROR > max_error:
        max_error = ERROR
print("no errors (max={})".format(max_error))
