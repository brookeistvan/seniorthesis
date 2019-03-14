import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_number = 2

Gammma = [2,4,6,8,10,12]
Beta = [2,4,6,8,10,12]

harvest = np.array([[127, 119, 120, 119, 126, 116],
                    [66, 65, 61, 62, 59, 60],
                    [48, 45, 42, 41, 40, 38],
                    [37, 33, 33, 33, 31, 30],
                    [30, 29, 26, 26, 25, 23],
                    [27, 24, 22, 21, 21, 21]])


fig, ax = plt.subplots()
im = ax.imshow(harvest)

# We want to show all ticks...
ax.set_xticks(np.arange(len(Beta)))
ax.set_yticks(np.arange(len(Gammma)))
# ... and label them with the respective list entries
ax.set_xticklabels(Beta)
ax.set_yticklabels(Gammma)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(Gammma)):
    for j in range(len(Beta)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

# ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.xlabel("Infection Rate (Beta)")
plt.ylabel("Recovery Rate (Gamma)")
plt.show()