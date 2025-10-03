#!/usr/bin/env python
import argparse
import matplotlib.pyplot as plt
import numpy as np
import math as m
import matplotlib.pyplot as plt

def R(theta):
    return np.array([
        [m.cos(theta), -m.sin(theta)],
        [m.sin(theta),  m.cos(theta)]
    ])

parser = argparse.ArgumentParser(
    description='Samples from position distribution and orientation'
    ' distribution and plots samples of camera positions and Gaussian'
    ' approximation'
)
parser.add_argument('--sigmaxx', type=float, default=0.05,
                     help='std dev along x-dimension, default=0.05')
parser.add_argument('--sigmayy', type=float, default=0.05,
                     help='std dev along y-diimension, default=0.05')
parser.add_argument('--mx', type=float, default=2.0,
                    help='mean of x component, default=2.0')
parser.add_argument('--my', type=float, default=3.0,
                    help='mean of y component, default=3.0')
parser.add_argument('--rho', type=float, default=-0.4,
                    help='correlation coefficient, default=-0.4')
parser.add_argument('--sigmatheta', type=float, default=0.5,
                    help='orientation standard deviation, default=0.5')
parser.add_argument('--theta', type=float, default=0.5,
                    help='orientation in radians, default=0.5 rad')
parser.add_argument('--tx', type=float, default=0.3,
                    help='camera x translation, default=0.3 m')
parser.add_argument('--ty', type=float, default=0.2,
                    help='camera x translation, default=0.2 m')
parser.add_argument('--numsamples', type=int, default=1500,
                    help='number of samples to generate, default=1500')
args = parser.parse_args()

mx = args.mx
my = args.my
theta = args.theta
sigma_xx = args.sigmaxx
sigma_yy = args.sigmayy
sigma_theta = args.sigmatheta
var_theta = sigma_theta ** 2
num_samples = args.numsamples
rho = args.rho
tx = args.tx
ty = args.ty
t = np.array([[tx],[ty]])
covariance = np.array([[sigma_xx ** 2, sigma_xx * sigma_yy * rho, 0],
                       [sigma_xx * sigma_yy * rho, sigma_yy ** 2, 0],
                       [0, 0, var_theta]])
mean = np.array([mx, my, theta])
robot_samples = np.random.multivariate_normal(mean, covariance, num_samples)
camera_samples = np.array([
    (R(theta) @ t + np.array([[x],[y]])).T[0]
    for x, y, theta in robot_samples
])

# transform the covariance using the expression derived in class
robot_pos_cov = covariance[0:2,0:2]
cam_pos_cov = robot_pos_cov + R(theta-m.pi/2)@t@t.T@R(m.pi/2-theta)*var_theta

# uncertainty ellipse
eigenvalues, eigenvectors = np.linalg.eig(cam_pos_cov)
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]
tt =  np.linspace(0, 2*np.pi, 100)
ellipse_points = np.array([np.cos(tt), np.sin(tt)])
scaled_ellipse = 3 * np.sqrt(eigenvalues)[:, np.newaxis] * ellipse_points
rotated_ellipse = np.dot(eigenvectors, scaled_ellipse)

plt.scatter(robot_samples[:, 0], robot_samples[:, 1], color='r', s=2, alpha=0.5)
plt.scatter(camera_samples[:, 0], camera_samples[:, 1], color='b', s=2, alpha=1)
plt.plot(mx + tx*m.cos(theta) - ty*m.sin(theta) + rotated_ellipse[0, :],
         my + tx*m.sin(theta) + ty*m.cos(theta) + rotated_ellipse[1, :],
         color='green')
plt.title(r'$\sigma_{xx}=' + f'{sigma_xx}' +
          r'\;\;\sigma_{yy}=' + f'{sigma_yy}' +
          r'\;\;\rho=' + f'{rho}' +
          r'\;\;\sigma_{\theta}=' + f'{sigma_theta}' +
          r'\;\;t_{x}=' + f'{tx}' +
          r'\;\;t_{y}=' + f'{ty}'
          '$')
plt.xlabel(r'$x_{1}$')
plt.ylabel(r'$x_{2}$')
plt.xlim(-5, 10)
plt.ylim(-5, 10)
plt.axis('equal')
plt.grid()
plt.show()
