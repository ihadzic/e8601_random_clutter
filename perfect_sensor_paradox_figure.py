import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


n_points = 1000
mean_cloud = [0, 0]
covariance_cloud = [[10, 6], [6, 8]]
x_cloud, y_cloud = np.random.multivariate_normal(mean_cloud, covariance_cloud, n_points).T
z_cloud = np.zeros(n_points)
mean_surface = [2, 2]
covariance_surface = [[1e-3, 0], [0, 1e-3]]  # Very small variance

x = np.linspace(1.5, 2.5, 100)
y = np.linspace(1.5, 2.5, 100)
x, y = np.meshgrid(x, y)

def gaussian_2d(x, y, mean, cov):
    pos = np.empty(x.shape + (2,))
    pos[:, :, 0] = x
    pos[:, :, 1] = y
    inv_cov = np.linalg.inv(cov)
    diff = pos - mean
    exponent = -0.5 * np.einsum('...k,kl,...l->...', diff, inv_cov, diff)
    z = np.exp(exponent) / (2 * np.pi * np.sqrt(np.linalg.det(cov)))
    return z/100

z = gaussian_2d(x, y, mean_surface, covariance_surface)

xlim = (-10, 10)
ylim = (-10, 10)
zlim = (-0.01, 1)

fig1 = plt.figure(figsize=(10, 8))
ax1 = fig1.add_subplot(111, projection='3d')
ax1.scatter(x_cloud, y_cloud, z_cloud, c='r', s=5, alpha=0.6)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.set_zlim(zlim)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
plt.show()

fig2 = plt.figure(figsize=(10, 8))
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(x_cloud, y_cloud, z_cloud, c='r', s=5, alpha=0.6)
ax2.plot_surface(x, y, z, cmap='viridis', alpha=0.8)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2.set_zlim(zlim)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
plt.show()
