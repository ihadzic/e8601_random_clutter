#!/usr/bin/env python
import argparse
import math
import matplotlib.pyplot as plt
import numpy as np

# Parameters for the 2D Gaussian distribution

parser = argparse.ArgumentParser(
    description='Plots the uncertainty ellipse and random samples of a'
    '2D Gaussian distribution, given the mean and covariance'
)
parser.add_argument('--sigmaxx', type=float, default=1.0,
                     help='std dev along x-diimension, default=1')
parser.add_argument('--sigmayy', type=float, default=2.0,
                     help='std dev along y-diimension, default=2')
parser.add_argument('--mx', type=float, default=2.0,
                    help='mean of x component, default=2.0')
parser.add_argument('--my', type=float, default=3.0,
                    help='mean of y component, default=3.0')
parser.add_argument('--rho', type=float, default=0.7,
                    help='correlation coefficient, default=0.7')
args = parser.parse_args()

mean = np.array([args.mx, args.my])
sigma_xx = args.sigmaxx
sigma_yy = args.sigmayy
rho = args.rho
covariance = np.array([[sigma_xx ** 2, sigma_xx * sigma_yy * rho], 
                       [sigma_xx * sigma_yy * rho, sigma_yy ** 2]])


# Compute eigenvalues and eigenvectors of the covariance matrix
eigenvalues, eigenvectors = np.linalg.eig(covariance)

# Sort eigenvalues and corresponding eigenvectors in descending order
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Generate 1000 realizations from the 2D Gaussian distribution
num_samples = 1500
samples = np.random.multivariate_normal(mean, covariance, num_samples)

# Plot the point cloud in the x, y plane
plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5)

# Calculate the angle of rotation for the ellipse
theta = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

# Generate points on the unit circle to form the ellipse
t = np.linspace(0, 2*np.pi, 100)
ellipse_points = np.array([np.cos(t), np.sin(t)])

# Transform the ellipse points to align with the eigenvectors and scale by the square root of eigenvalues
scaled_ellipse = 3 * np.sqrt(eigenvalues)[:, np.newaxis] * ellipse_points
rotated_ellipse = np.dot(eigenvectors, scaled_ellipse)

# Plot the uncertainty ellipse
plt.plot(mean[0] + rotated_ellipse[0, :], mean[1] + rotated_ellipse[1, :], color='red')

# Plot eigenvectors as arrows
plt.quiver(mean[0], mean[1], eigenvectors[0, 0], eigenvectors[1, 0], angles='xy', scale_units='x', scale=0.3, color='blue')
plt.quiver(mean[0], mean[1], eigenvectors[0, 1], eigenvectors[1, 1], angles='xy', scale_units='x', scale=0.3, color='blue')

print(eigenvectors)

# Draw x and y axes
plt.axhline(0, color='green', linewidth=1.5)
plt.axvline(0, color='green', linewidth=1.5)

plt.title(r'$\sigma_{xx}=' + f'{sigma_xx}' +
          r'\;\;\sigma_{yy}=' + f'{sigma_yy}' +
          r'\;\;\rho=' + f'{rho}' + '$')
plt.xlabel(r'$x_{1}$')
plt.ylabel(r'$x_{2}$')
plt.xlim(-5, 10)
plt.ylim(-5, 10)
plt.axis('equal')
plt.grid()

# Show the plot
plt.show()
