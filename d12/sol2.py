import numpy as np

res2 = np.lcm.reduce(np.array([2028, 5898, 4702], dtype=object))
res = np.lcm.reduce(np.array([186028, 161428, 144624], dtype=object))
print(res, res2)
