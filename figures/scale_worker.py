import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
partition = np.array([1, 2, 4, 8, 16, 32], dtype=np.int)
gupt_error = np.array([800, 700, 620, 560, 540, 530], dtype=np.float)
naive_error = np.array([660, 580, 520, 480, 450, 430], dtype=np.float)
combine_error = np.array([700, 600, 540, 520, 490, 480], dtype=np.float)

axes = plt.gca()
# axes.set_ylim([0, 100])

# red dashes, blue squares and green triangles
plt.plot(partition, gupt_error, '*-', label="Gigraph")
plt.plot(partition, naive_error, 'x-', label="PowerGraph")
plt.plot(partition, combine_error, 'v-', label="GraphX")

plt.ylabel("Time (s)")
plt.xlabel("Number of Worker")
legend = axes.legend(loc='upper right', shadow=False)

plt.savefig('scale_worker.pdf', format='pdf', dpi=500)
