import matplotlib.pyplot as plt

# Datenpunkte
yolo11 = [(1.5,39.5),(2.5,47),(4.7,51.5),(6.2,53.4),(11.3,54.7)]
yolo10 = [(1.56,39.5),(2.66,46.7),(5.48,51.3),(6.54,52.7),(8.33,53.3),(12.2,54.4)]
yolo9 = [(2.3,38.3),(3.54,46.8),(6.43,51.4),(7.16,53),(16.77,55.6)]
yolo8 = [(1.47,37.3),(2.66,44.9),(5.86,50.2),(9.06,52.9),(14.37,53.9)]

# Aufteilen in x- und y-Werte
x11, y11 = zip(*yolo11)
x10, y10 = zip(*yolo10)
x9, y9 = zip(*yolo9)
x8, y8 = zip(*yolo8)

# Stil gemäß den früheren Plots
plt.figure(figsize=(12, 6))
plt.plot(x11, y11, 'o-', label="YOLOv11", alpha=0.4, linewidth=3)
plt.plot(x10, y10, 'o-', label="YOLOv10", alpha=0.4, linewidth=3)
plt.plot(x9, y9, 'o-', label="YOLOv9", alpha=0.4, linewidth=3)
plt.plot(x8, y8, 'o-', label="YOLOv8", alpha=0.4, linewidth=3)

# Achsenbeschriftungen im LaTeX-Stil
plt.xlabel(r"$\mathit{Latency\,T4\,TensorRT10\,FP16\ in\ ms/Bild}$", fontsize=16)
plt.ylabel(r"$\mathit{COCO\,mAP\,50{-}95}$", fontsize=16)

# Achsenticks
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Achsenbereich
plt.xlim(0, 18)
plt.ylim(36, 56)

# Legende
plt.legend(fontsize=14)

# Gitter & Layout
plt.grid(True)
plt.tight_layout()

# Speichern als SVG
plt.savefig("yolo_performance.svg", format="svg")

# Anzeigen
plt.show()
