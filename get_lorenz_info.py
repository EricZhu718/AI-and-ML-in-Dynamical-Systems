import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D


np.set_printoptions(threshold=sys.maxsize)

# returns a matrix with each entry being the time, x, y, and z values of the lorenz
def get_lorenz_vals(endTime, timeStep, rho, sigma, beta, state0):

    # differential form
    def f(state, t):
        x, y, z = state  # Unpack the state vector
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives


    t = np.arange(0.0, endTime, timeStep)
    states = odeint(f, state0, t)
    t = np.transpose(t)
    states = np.insert(states, 0, t, axis=1)
    return states

# returns a matrix with each entry being the time, x, y, and z values of the lorenz
def get_lorenz_vals_default_constants(endTime, timeStep, state0):
    rho = 18.0
    sigma = 10.0
    beta = 8.0 / 3.0

    # differential form
    def f(state, t):
        x, y, z = state  # Unpack the state vector
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z  # Derivatives

    t = np.arange(0.0, endTime, timeStep)
    states = odeint(f, state0, t)
    t = np.transpose(t)
    states = np.insert(states, 0, t, axis=1)
    return states

if __name__ == '__main__':
    print(np.asarray(get_lorenz_vals_default_constants(40, 0.01, [1.0, 1.0, 1.0])))
    print(np.asarray(get_lorenz_vals(40, 0.01, 18, 10, 8.0/3, [1.0, 1.0, 1.0])))


