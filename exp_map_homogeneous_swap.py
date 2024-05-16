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

def random_transform_matrix():
    krand = (random.random(), random.random(), random.random())
    krand /= numpy.linalg.norm(krand)
    theta = random.random()*math.pi
    k = numpy.array([krand]).transpose()
    x, y, z, = (random.random(), random.random(), random.random())
    random_transformation = numpy.identity(4)
    random_transformation[0, 3] = x
    random_transformation[1, 3] = y
    random_transformation[2, 3] = z
    random_transformation[0:3, 0:3] = rodrigues(krand, theta)
    return random_transformation

def adjoint(T):
    sst = skew_sim_mat(T[0, 3], T[1, 3], T[2, 3])
    adjT = numpy.zeros((6, 6))
    adjT[0:3, 0:3] = T[0:3, 0:3]
    adjT[3:6, 3:6] = T[0:3, 0:3]
    adjT[3:6, 0:3] = sst @ T[0:3, 0:3]
    return adjT

def exp_mapping(linear, angular):
    if angular == (0, 0, 0):
        em = numpy.identity(4)
        em[0, 3] = linear(0)
        em[1, 3] = linear(1)
        em[2, 3] = linear(2)
        return em
    theta = numpy.linalg.norm(angular)
    komega = numpy.array((angular)).transpose() / theta
    emkomega = skew_sim_mat(*angular) / theta
    kv = numpy.array([linear]).transpose() / theta
    G = numpy.identity(3) * theta + \
        (1 - math.cos(theta)) * emkomega + \
        (theta - math.sin(theta)) * (emkomega @ emkomega)
    Gkv = G @ kv
    em = numpy.identity(4)
    em[0:3, 0:3] = rodrigues(komega, theta)
    em[0, 3] = Gkv[0][0]
    em[1, 3] = Gkv[1][0]
    em[2, 3] = Gkv[2][0]
    return em

for _ in range(10000):
    T = random_transform_matrix()
    adjT = adjoint(T)
    random_lin = (random.random(), random.random(), random.random())
    random_ang = (random.random(), random.random(), random.random())

    left = T @ exp_mapping(random_lin, random_ang)

    AAA = adjT @ numpy.array([random_ang + random_lin]).transpose()
    Alin=tuple(AAA[3:6, 0])
    Aang=tuple(AAA[0:3, 0])
    right = exp_mapping(Alin, Aang) @ T

    E = numpy.linalg.norm(right - left)
    if E > 1e-8:
        print('ding ding ding error')
        exit(1)
print('no errors')
