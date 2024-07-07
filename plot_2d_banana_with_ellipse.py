#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import math

def sample_motion_model_odometry(u_t0, u_t1, x_t0, alpha):
    """
    Generates a new pose sample given the previous pose, odometry measurements, and noise parameters.
    
    Parameters:
    u_t0 -- the previous odometry reading (x, y, theta)
    u_t1 -- the current odometry reading (x, y, theta)
    x_t0 -- the previous pose (x, y, theta)
    alpha -- noise parameters for the motion model
    
    Returns:
    x_t1 -- the new pose sample (x, y, theta)
    """
    # Compute the changes in odometry
    delta_rot1 = np.arctan2(u_t1[1] - u_t0[1], u_t1[0] - u_t0[0]) - u_t0[2]
    delta_trans = np.sqrt((u_t1[0] - u_t0[0])**2 + (u_t1[1] - u_t0[1])**2)
    delta_rot2 = u_t1[2] - u_t0[2] - delta_rot1
    
    # Add noise to the odometry measurements
    delta_rot1_hat = delta_rot1 + np.random.normal(0, alpha[0] * abs(delta_rot1) + alpha[1] * delta_trans)
    delta_trans_hat = delta_trans + np.random.normal(0, alpha[2] * delta_trans + alpha[3] * (abs(delta_rot1) + abs(delta_rot2)))
    delta_rot2_hat = delta_rot2 + np.random.normal(0, alpha[0] * abs(delta_rot2) + alpha[1] * delta_trans)
    
    # Compute the new pose
    x_t1 = np.zeros(3)
    x_t1[0] = x_t0[0] + delta_trans_hat * np.cos(x_t0[2] + delta_rot1_hat)
    x_t1[1] = x_t0[1] + delta_trans_hat * np.sin(x_t0[2] + delta_rot1_hat)
    x_t1[2] = x_t0[2] + delta_rot1_hat + delta_rot2_hat
    
    return x_t1

# Parameters for the motion model
alpha = [0.07, 0.07, 0.02, 0.02]

# Initial pose
x_t0 = np.array([0, 0, 0])

# Odometry readings (example values)
u_t0 = np.array([2, 3, 0])
u_t1 = np.array([4, 6, np.pi/4])

# Generate samples
num_samples = 1500
samples = np.zeros((num_samples, 3))
for i in range(num_samples):
    samples[i] = sample_motion_model_odometry(u_t0, u_t1, x_t0, alpha)

cov_mat = np.cov(samples[:, 0:2].transpose())
print(cov_mat)
sigma_xx = round(cov_mat[0,0],2)
sigma_yy = round(cov_mat[1,1],2)
rho = round(cov_mat[0, 1] / (math.sqrt(cov_mat[0,0] * cov_mat[1,1])),2)

# Fit PCA to the generated samples to find the best-fitting ellipse
pca = PCA(n_components=2)
pca.fit(samples[:, :2])
eigenvalues = pca.explained_variance_
eigenvectors = pca.components_

# Plot the point cloud in the x, y plane
plt.scatter(samples[:, 0], samples[:, 1], alpha=0.5)

# Generate points on the unit circle to form the ellipse
t = np.linspace(0, 2 * np.pi, 100)
ellipse_points = np.array([np.cos(t), np.sin(t)])

# Transform the ellipse points to align with the eigenvectors and scale by the square root of eigenvalues
scaled_ellipse = 2 * np.sqrt(eigenvalues)[:, np.newaxis] * ellipse_points
rotated_ellipse = np.dot(eigenvectors.T, scaled_ellipse)

# Plot the uncertainty ellipse
plt.plot(pca.mean_[0] + rotated_ellipse[0, :], pca.mean_[1] + rotated_ellipse[1, :], color='red')

# Plot eigenvectors as arrows
plt.quiver(pca.mean_[0], pca.mean_[1], eigenvectors[0, 0], eigenvectors[0, 1], angles='xy', scale_units='xy', scale=1, color='blue')
plt.quiver(pca.mean_[0], pca.mean_[1], eigenvectors[1, 0], eigenvectors[1, 1], angles='xy', scale_units='xy', scale=1, color='blue')

print(eigenvectors)

# Draw x and y axes
plt.axhline(0, color='green', linewidth=1.5)
plt.axvline(0, color='green', linewidth=1.5)

plt.title(r'$\sigma_{xx}=' + f'{sigma_xx}' +
          r'\;\;\sigma_{yy}=' + f'{sigma_yy}' +
          r'\;\;\rho=' + f'{rho}' +
          r'\;\;\alpha=' + f'{alpha}' + '$')
plt.xlabel(r'$x_{1}$')
plt.ylabel(r'$x_{2}$')
plt.axis('equal')
plt.grid()

# Show the plot
plt.show()
