import numpy as np
from sklearn.neighbors import KDTree

import get_lorenz_info


class kNearestNeighborCenterOfMassApprox:
    tree = None
    k = 10
    dim = None
    last_point = None
    data_points = None

    def __init__(self, current_points, k=10):
        # current_points must be a n by dim+1 matrix with the first column timestamps
        from sklearn.neighbors import KDTree
        X = current_points[:, 1:len(current_points[0]) + 1]
        self.tree = KDTree(X, leaf_size=2)
        self.k = k
        self.dim = len(current_points[0]) - 1
        self.data_points = current_points

    def approx(self, steps, k=k):
        resultant_points = [[0] * self.dim] * steps
        prev_point = self.data_points[len(self.data_points) - 1][1:self.dim + 1]
        for x in range(steps):
            indices = self.tree.query([prev_point], self.k, return_distance=False)
            cm_change = [0] * self.dim
            valid_points = 0
            for index in indices[0]:
                if index + 1 < len(self.data_points):
                    valid_points += 1
                    for y in range(self.dim):
                        cm_change[y] += self.data_points[index + 1][y + 1] - self.data_points[index][y + 1]

            if valid_points > 0:
                for y in range(len(cm_change)):
                    cm_change[y] /= valid_points
            for y in range(self.dim):
                prev_point[y] += cm_change[y]
            resultant_points[x] = prev_point.copy()
            # print(prev_point)
            # print(x)
            # print()
        # print(resultant_points)
        return resultant_points


if __name__ == '__main__':
    approx = \
        kNearestNeighborCenterOfMassApprox(
            get_lorenz_info.get_lorenz_vals_default_constants(30, 0.001, [1, 1, 1]))
    for element in approx.approx(100):
        print(element)
