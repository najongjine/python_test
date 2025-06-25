import matplotlib.pyplot as plt
import numpy as np

# x와 y 값을 모두 지정
xpoints = np.array([10, 20, 30, 40])  # 원하는 x값
ypoints = np.array([3, 8, 1, 10])

plt.plot(xpoints, ypoints, marker='o',linestyle = 'dotted')  # x, y 모두 지정
plt.show()