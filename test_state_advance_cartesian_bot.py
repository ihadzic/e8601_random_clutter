#!/usr/bin/env python3
from cartesian_bot_kf import CartesianBotKF
import matplotlib.pyplot as plt
import numpy

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

botkf = CartesianBotKF(K, J, b, R, L, r)
botkf.set_state(0)
t = t_step
all_omega_x = []
all_omega_y = []
all_pos_x = []
all_pos_y = []
all_t = [i * t_step for i in range(1, 101)]
for t in all_t:
    vx = 10 if t < 4 else 0
    vy = 5 if t < 7 and t > 2 else 0
    botkf.simulate_system(t, vx, vy)
    omega_x, omega_y = botkf.peek_omega()
    pos_x, pos_y = botkf.peek_pos()
    all_omega_x.append(omega_x)
    all_omega_y.append(omega_y)
    all_pos_x.append(pos_x)
    all_pos_y.append(pos_y)
    i_x, _ = botkf.peek_current()
plt.subplot(221)
plt.plot(all_t, all_omega_x)
plt.grid()
plt.title('angular velocity -- x')
plt.xlabel('t [s]')
plt.ylabel(u'\u03c9x [rad/s]')
plt.axis([0, 10, 0, 1])
plt.subplot(222)
plt.plot(all_t, all_omega_y)
plt.grid()
plt.title('angular velocity -- y')
plt.ylabel(u'\u03c9y [rad/s]')
plt.xlabel('t [s]')
plt.axis([0, 10, 0, 1])

plt.subplot(223)
plt.plot(all_t, all_pos_x)
plt.grid()
plt.title('position -- x')
plt.ylabel('x [m]')
plt.xlabel('t [s]')
plt.axis([0, 10, 0, 1])
plt.subplot(224)
plt.plot(all_t, all_pos_y)
plt.grid()
plt.title('position -- y')
plt.ylabel('y [m]')
plt.xlabel('t [s]')
plt.axis([0, 10, 0, 1])

plt.show()
