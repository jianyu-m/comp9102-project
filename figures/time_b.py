import numpy as np
import matplotlib.pyplot as plt

N = 3
# twitter wordcount wordgrep connectedComponent SparkTC
# 2.125 4.25 3.52 1.91 1.609 2.4 2.91 = 2.67 1.67(61% - 3.25)
data = np.array([13, 10, 11], dtype=np.float)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, data, width, color='#FEFFBF', edgecolor='#000000', yerr=0)
# add some text for labels, title and axes ticks
ax.set_ylabel('Execution Time (s)', fontsize=14)
# ax.set_title('Scores by group and gender')
ax.set_xticks(ind)
ax.set_xticklabels(("Gigraph", "PowerGraph", "GraphX"))

# ax.legend((rects1[0], rects2[0], rects3[0]), ('Giraph', 'PowerGraph', 'GraphX'), frameon=False, fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=11)

# autolabel(rects1)
# autolabel(rects2)
plt.savefig('time_b.pdf', format='pdf', dpi=500)
