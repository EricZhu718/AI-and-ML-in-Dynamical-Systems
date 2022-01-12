import math

import numpy as np
from numpy.linalg import eig
from scipy.linalg import norm
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from random import random
from sklearn.linear_model import LinearRegression
import math


rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0

state0 = [1.0, 1.0, 1.0]
step_size = 0.001
time_bound = 50  # anything past this time will be approximated
predict_to_time = 60

radius = 0.75

def f(state, t):
    x, y, z = state  # Unpack the state vector
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives


t = np.arange(0.0, time_bound, step_size)


states = np.array(odeint(f, state0, t))
# print(states)

# returns a boolean with true meaning that the point is within the sphere

def trajectories(radius, x_center, y_center, z_center, states):
    def contains(point):
        return math.sqrt(
            math.pow(point[0] - x_center, 2) + math.pow(point[1] - y_center, 2) + math.pow(point[2] - z_center, 2)) < radius
    trajectories = []  # each entry is a trajectory contained within the ball
    if contains(states[0]):
        trajectories.append([[states[0][0], states[0][1], states[0][2], 0]])
    for x in range(1, len(states)):
        # print(states[x])
        if contains(states[x-1]) and contains(states[x]) and x*step_size <= time_bound:
            trajectories[len(trajectories)-1].append([states[x][0], states[x][1], states[x][2], x * step_size])
        elif contains(states[x]) and x*step_size <= time_bound:
            trajectories.append([])
            trajectories[len(trajectories)-1].append([states[x][0], states[x][1], states[x][2], x * step_size])
    return trajectories


points_recorded = len(states)

# approximates time
time = time_bound + step_size
prev_point = states[len(states)-1]
approx_points = []
while time <= predict_to_time:
    trajs_in_sphere = trajectories(radius, prev_point[0], prev_point[1], prev_point[2], states)

    num_of_diff = 0
    for trajectory in trajs_in_sphere:
        num_of_diff += len(trajectory)-1

    avg_dis = [0 for x in range(0, len(trajs_in_sphere[0][0])-1)]  # tracks the average displacement vector for each trajectory
    for trajectory in trajs_in_sphere:
        if len(trajectory) > 1:
            for x in range(1, len(trajectory)):
                for coordinate in range(0, len(trajectory[x])-1):
                    avg_dis[coordinate] += (trajectory[x][coordinate]-trajectory[x-1][coordinate]) / num_of_diff
    # print(avg_dis)
    prev_point = [prev_point[x] + avg_dis[x] for x in range(0, len(trajs_in_sphere[0][0])-1)]
    approx_points.append(prev_point)
    time += step_size
    print(time)


def distance(point1, point2):
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2) + math.pow(point1[2] - point2[2], 2))


difference = []

t = np.arange(time_bound + step_size, predict_to_time, step_size)
state0 = states[len(states)-1]
states_new = np.array(odeint(f, state0, t))
for x in range(0, len(approx_points)):
    difference.append([time_bound + step_size * x, distance(approx_points[x], states_new[x])])
difference = np.array(difference)
fig, ax = plt.subplots(1)
ax.set_title("Error rate (distance)")
ax.plot(difference[:, 0], difference[:, 1])


fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
ax1.set_title("X vs time for approx")
ax1.plot(t, np.asarray(approx_points)[:, 0], label='approx')
ax1.plot(t, np.asarray(states_new)[:, 0], label='real')
ax2.set_title("Y vs time for approx")
ax2.plot(t, np.asarray(approx_points)[:, 1], label='approx')
ax2.plot(t, np.asarray(states_new)[:, 1], label='real')
ax3.set_title("Z vs time for approx")
ax3.plot(t, np.asarray(approx_points)[:, 2], label='approx')
ax3.plot(t, np.asarray(states_new)[:, 2], label='real')

plt.draw()
plt.show()

