import numpy as np
import math

x = np.array([[0, 2, 4],
[1, 3, 5]]) # (2,3)
cols = x.sum(axis=0)
print(np.sin(x[0:1, 0:1]))
print(cols.ndim)