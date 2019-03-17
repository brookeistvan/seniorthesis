import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_number = 2

a = np.arange(11*5*5).reshape(11,5,5)
print(a)
print(a.mean(axis=(1,2)))

Gammma = [2,4,6,8,10,12]
Beta = [2,4,6,8,10,12]

harvest = np.array([127, 119, 120, 119, 126, 116, 66, 65, 61, 62, 59, 60, 48, 45, 42, 41, 40, 38,37, 33, 33, 33, 31, 30, 30, 29, 26, 26, 25, 23, 27, 24, 22, 21, 21, 21])

mesemap2 = harvest.reshape(3,2,6)
print(mesemap2)
mesemap1 = np.array([harvest[i:i+6] for i in range(0, len(harvest), 6)])
mesemap = np.array([mesemap1[j:j+2] for j in range(0, len(mesemap1), 2)])
print(mesemap)

b = mesemap.mean(axis=(1,2))
print(b)
print(mesemap.mean(axis=1))

# fig, ax = plt.subplots()
# im = ax.imshow(mesemap)

# # We want to show all ticks...
# ax.set_xticks(np.arange(len(Beta)))
# ax.set_yticks(np.arange(len(Gammma)))
# # ... and label them with the respective list entries
# ax.set_xticklabels(Beta)
# ax.set_yticklabels(Gammma)

# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")

# # Loop over data dimensions and create text annotations.
# for i in range(len(Gammma)):
#     for j in range(len(Beta)):
#         text = ax.text(j, i, mesemap[i, j],
#                        ha="center", va="center", color="w")

# # ax.set_title("Harvest of local farmers (in tons/year)")
# fig.tight_layout()
# plt.xlabel("Infection Rate (Beta)")
# plt.ylabel("Recovery Rate (Gamma)")
# plt.show()