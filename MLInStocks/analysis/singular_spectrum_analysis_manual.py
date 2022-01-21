import math

import numpy as np
from numpy.linalg import eig
from scipy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from random import random


rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

lag_back = 10  # goes from t to t-(lag_back - 1)*tau
state0 = [1.0, 1.0, 1.0]
step_size = 0.01
sharey = True

static_mag = 0


def f(state, t):
    x, y, z = state  # Unpack the state vector
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives


t = np.arange(0.0, 40.0, step_size)


states = np.array(odeint(f, state0, t))

# adds static to states
for x in states:
    x[0] += static_mag * random()

iterations = 0
X_matrix = []
for r_vec in states:
    iterations += 1
    if len(states) - iterations + 1 >= lag_back:
        row = []
        for x in range(1, lag_back + 1):
            # print(x)
            # print(iterations+x-2)
            row.append(states[iterations + x - 2][0])
        # print(len(row))
        X_matrix.append(row)

# print(X_matrix)

Xi = np.transpose(X_matrix) @ X_matrix
# print(Xi)

eign_vals, eign_vecs_normal = eig(Xi)
eign_vecs_normal = np.transpose(eign_vecs_normal)
# print(len(eign_vecs_normal))
# print("eigenvalues: "+str(eign_vals))
non_zero_eign_vecs = []
num_of_non_zero_eign_vecs = 0

# graphs the eigenvalues
fig, ax = plt.subplots(1)
ax.set_title("Eigenvalues")
eign_vals_adjust = eign_vals.copy()
sum_of_val = 0
for val in eign_vals:
    sum_of_val += val
for x in range(0, len(eign_vals)):
    eign_vals_adjust[x] = math.log10(eign_vals[x]/sum_of_val)

ax.plot(range(1, len(eign_vals) + 1), eign_vals_adjust)
# plt.yscale("log")
plt.ion()
plt.draw()
plt.pause(0.5)
plt.show(block=False)

plt.pause(2)

for x in range(0, int(input("Enter the number of eigenvectors you want:"))):

    non_zero_eign_vecs.append(eign_vecs_normal[x])
    num_of_non_zero_eign_vecs += 1

non_zero_eign_vecs = np.transpose(non_zero_eign_vecs)

# print("eigenvalues:")
# print(eign_vals)

noise_removed = np.array(X_matrix) @ np.array(non_zero_eign_vecs)
# print(noise_removed)
# print(len(np.transpose(non_zero_eign_vecs)))

# plots the projections
plt.yscale("linear")
fig, ax = plt.subplots(len(non_zero_eign_vecs[0]), sharex=True, sharey=sharey)
fig.suptitle("Projections")
for x in range(0, len(non_zero_eign_vecs[0])):
    # print(norm(non_zero_eign_vecs[:, x]))
    ax[x].plot(np.array(range(0, len(X_matrix))) * step_size, noise_removed[:, x])


# plots the eigenvectors
fig, ax = plt.subplots(len(non_zero_eign_vecs[0]), sharex=True, sharey=sharey)
fig.suptitle("Eigenvectors")
for x in range(0, len(non_zero_eign_vecs[0])):
    ax[x].plot(np.array(range(1, len(non_zero_eign_vecs) + 1)), non_zero_eign_vecs[:, x])

# plots the original, reconstructed, and combo graphs
fig, (original, reconstructed, combo) = plt.subplots(3, sharex=True)
original.set_title("Original")
original.plot(np.arange(0.0, 40.0, step_size), states[:, 0])

noise_removed_sum = noise_removed @ (np.zeros(len(noise_removed[0])) + 1)
# reconstructed.set_title("Reconstructed")
# reconstructed.plot(np.array(range(0, len(X_matrix))) * step_size, noise_removed_sum)

combo.set_title("Combined")
# combo.plot(np.arange(0.0, 40.0, step_size), states[:, 0])
# combo.plot(np.array(range(0, len(X_matrix))) * step_size, noise_removed_sum)

# draws a bunch of c_i by c_j plots
for x in range(0, len(non_zero_eign_vecs[0]) - 1):
    for y in range(x + 1, len(non_zero_eign_vecs[0])):
        # print(x, y)
        fig, ax = plt.subplots(1)
        ax.plot(X_matrix @ non_zero_eign_vecs[:, x], X_matrix @ non_zero_eign_vecs[:, y])
        ax.set_title("c_" + str(x) + " by c_" + str(y))

if len(non_zero_eign_vecs[0]) >= 3:
    # draws 3d plot of the 3 eigenvectors with the highest eigenvalues
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    ax.plot(X_matrix @ non_zero_eign_vecs[:, 0], X_matrix @ non_zero_eign_vecs[:, 1], X_matrix @ non_zero_eign_vecs[:, 2])
    ax.set_title("c_0 by c_1 by c_2")

# plots original 3d lorenz
fig = plt.figure()
ax = fig.gca(projection="3d")
ax.set_title("Original Lorenz")
ax.plot(states[:, 0], states[:, 1], states[:, 2])

plt.draw()
plt.show(block=True)

