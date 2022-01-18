import numpy as np
from matplotlib import pyplot as plt
from pyts.decomposition import SingularSpectrumAnalysis
import get_lorenz_info as lz
import random
import json







if __name__ == '__main__':
    full_lorenz = lz.get_lorenz_vals_default_constants(10, 0.01, [1, 1, 1])

    lorenz_x = np.copy(full_lorenz[:, 1])

    random.seed(a=1, version=2)
    for x in range(len(lorenz_x)):
        # adds random noise
        lorenz_x[x] += random.random()*10

    timeVals = full_lorenz[:, 0]

    window_size = 20
    groups = 10
    ssa = SingularSpectrumAnalysis(window_size=window_size, groups=groups)
    X_ssa = ssa.fit_transform([lorenz_x])

    print(json.loads(X_ssa))
    plt.figure(figsize=(16, 6))
    ax1 = plt.subplot(121)
    ax1.plot(timeVals, full_lorenz[:, 1])

    ax2 = plt.subplot(122)
    for x in range(groups):
        ax2.plot(timeVals, X_ssa[len(X_ssa)-1-x])

    plt.draw()
    plt.show()

