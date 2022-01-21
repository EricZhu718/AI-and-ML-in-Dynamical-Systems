import numpy as np
from matplotlib import pyplot as plt
from pyts.decomposition import SingularSpectrumAnalysis
import json

if __name__ == '__main__':

    # loads a json object with y keys
    json_object = (json.loads(input()))

    values = []
    for line in json_object:
        values.append(line['y'])
    ssa = SingularSpectrumAnalysis(window_size=int(input()), groups=int(input()))
    X_ssa = ssa.fit_transform([values])
    print(json.dumps(X_ssa.tolist()))

