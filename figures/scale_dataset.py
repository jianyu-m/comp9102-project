import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
partition = np.array([1, 2, 4, 8, 16, 32], dtype=np.int)
gupt_error = np.array([18, 32, 55, 79, 61, 64], dtype=np.float)
naive_error = np.array([18, 33, 55, 79, 62, 64], dtype=np.float)
combine_error = np.array([16, 16, 40, 84, 63, 64], dtype=np.float)

axes = plt.gca()
axes.set_ylim([0, 100])

# red dashes, blue squares and green triangles
plt.plot(partition, gupt_error, '*-', label="Gigraph")
plt.plot(partition, naive_error, 'x-', label="PowerGraph")
plt.plot(partition, combine_error, 'v-', label="GraphX")

plt.ylabel("Time (s)")
plt.xlabel("Number of Worker")
legend = axes.legend(loc='upper right', shadow=False)

plt.savefig('scale_dataset.pdf', format='pdf', dpi=500)
