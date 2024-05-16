#!/usr/bin/env python3
from cartesian_bot_kf import CartesianBotKF
import matplotlib.pyplot as plt
import numpy
import math

# motor parameters
K = 0.01
J = 0.01
b = 0.1
R = 1
L = 0.5

# wheel radius
r = 0.25

# time stemp
t_step = 0.1

bot_model = CartesianBotKF(K, J, b, R, L, r)
bot_model.set_state(0)

estimator = CartesianBotKF(K, J, b, R, L, r)
estimator.set_state(0)

vx_variance = 0.1
vy_variance = 0.2
t = t_step
all_t = [i * t_step for i in range(1, 101)]

# input x voltage with noise
vx_nominal = [10 if t < 4 else 0 for t in all_t]
vx = [v+n for v, n in zip(vx_nominal, list(numpy.random.normal(0, math.sqrt(vx_variance), len(all_t))))]

# input y voltage with noise
vy_nominal = [5 if t < 7 and t > 2 else 0 for t in all_t]
vy = [v+n for v, n in zip(vy_nominal, list(numpy.random.normal(0, math.sqrt(vx_variance), len(all_t))))]

x_ground_truth = []
y_ground_truth = []
for i in range(len(all_t)):
    # move the system under simulation using noisy input
    bot_model._predict(all_t[i], vx[i], vy[i])
    bot_model._skip_measure()
    xgt, ygt = bot_model._peek_pos()
    x_ground_truth.append(xgt)
    y_ground_truth.append(ygt)

plt.figure(1)

plt.title('input voltages (with noise)')
plt.subplot(211)
plt.plot(all_t, vx)
plt.xlabel('t [s]')
plt.ylabel('Vx [V]')
plt.axis([0, 10, -1, 11])
plt.grid()

plt.subplot(212)
plt.plot(all_t, vy)
plt.xlabel('t [s]')
plt.ylabel('Vy [V]')
plt.axis([0, 10, -1, 11])
plt.grid()

plt.figure(2)
plt.title('robot position: ground truth (blue)')
plt.subplot(211)
plt.plot(all_t, x_ground_truth)
plt.xlabel('t [s]')
plt.ylabel('x [m]')
plt.grid()

plt.subplot(212)
plt.plot(all_t, y_ground_truth)
plt.xlabel('t [s]')
plt.ylabel('y [m]')
plt.grid()

plt.figure(3)
plt.scatter(x_ground_truth, y_ground_truth, s=4)
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.grid()

plt.show()
