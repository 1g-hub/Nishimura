import matplotlib.pyplot as plt
import numpy as np
#単目的 GA
fp1 = 0.44933
fw1 = 0.85146
fc1 = 0.36788
#多目的 GA
fp2 = 0.66365
fw2 = 0.79097
fc2 = 0.42035
#提案手法
fp3 = 0.53259
fw3 = 0.80783
fc3 = 0.44933

fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(fp1, fw1, fc1, color='green')
ax.scatter(fp2, fw2, fc2, color='red')
ax.scatter(fp3, fw3, fc3, color='blue')

ax.set_xlabel('Fitness (Magnitude of Changes)')
ax.set_ylabel('Fitness (Win Rate)')
ax.set_zlabel('Fitness (Number of Changed Card)')

#ax.legend()

plt.savefig("jikken4.png", format="png", dpi=300)