import matplotlib.pyplot as plt
import cv2
import os

# Bilder laden und in RGB konvertieren
image_paths = [
    "E:\\Workspace\\Masterarbeit\\Plots\\Disskusion\\A9_run3.png",      # a)
    "E:\\Workspace\\Masterarbeit\\Plots\\Disskusion\\E7_run3.png"       # c)
]
images = [cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB) for img in image_paths]

# Zielpfad für das Speichern als SVG
output_path = "E:\\Workspace\\Masterarbeit\\Plots\\Disskusion\\Disskusion2_run3.svg"

# Plot erstellen
fig, axes = plt.subplots(1, 2, figsize=(6, 12))
labels = ['a)', 'b)']

for ax, img, label in zip(axes, images, labels):
    ax.imshow(img)
    ax.set_title(label, fontsize=14, fontweight='bold', loc='left')
    ax.axis('off')

plt.tight_layout()
fig.savefig(output_path, format='svg', bbox_inches='tight')
plt.show()
