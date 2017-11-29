import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
partition = np.array([0, 1, 2, 3, 4, 5], dtype=np.int)
gupt_error = np.array([180, 190, 220, 252, 295, 350], dtype=np.float)
naive_error = np.array([140, 160, 186, 200, 230, 270], dtype=np.float)
combine_error = np.array([160, 180, 210, 246, 280, 320], dtype=np.float)

# locs, labels = xticks()

plt.xticks(range(6), ('20M', '40M', '60M', '80M', '100M', '120M') )

# 130million / 100 million / 80 million / 60 million / 40 million / 20 mullion
axes = plt.gca()
axes.set_ylim([120, 450])

# red dashes, blue squares and green triangles
plt.plot(partition, gupt_error, '*-', label="Gigraph")
plt.plot(partition, naive_error, 'x-', label="PowerGraph")
plt.plot(partition, combine_error, 'v-', label="GraphX")

plt.ylabel("Time (s)")
plt.xlabel("Number of Edges")
legend = axes.legend(loc='upper right', shadow=False)

plt.savefig('scale_dataset.pdf', format='pdf', dpi=500)
