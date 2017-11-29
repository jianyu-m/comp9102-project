import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
partition = np.array([1, 2, 3, 4, 5, 6], dtype=np.int)
gupt_error = np.array([180, 200, 220, 240, 250, 560], dtype=np.float)
naive_error = np.array([140, 160, 180, 210, 240, 480], dtype=np.float)
combine_error = np.array([160, 180, 220, 230, 260, 520], dtype=np.float)


# billion / 100 million / 80 million / 60 million / 40 million / 20 mullion
axes = plt.gca()
# axes.set_ylim([0, 100])

# red dashes, blue squares and green triangles
plt.plot(partition, gupt_error, '*-', label="Gigraph")
plt.plot(partition, naive_error, 'x-', label="PowerGraph")
plt.plot(partition, combine_error, 'v-', label="GraphX")

plt.ylabel("Time (s)")
plt.xlabel("Number of Worker")
legend = axes.legend(loc='upper right', shadow=False)

plt.savefig('scale_dataset.pdf', format='pdf', dpi=500)
