import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Neue Metriken vorbereiten
data = {
    "Label": ["A1", "A5", "A9", "C1", "C5", "C9", "E1", "E5", "E9"],
    "Precision": [1.0000, 0.5769, 0.4286, 1.0000, 1.0000, 0.6667, 0.5556, 0.3421, 0.8667],
    "Recall": [0.8667, 1.0000, 0.2000, 0.2667, 1.0000, 0.8000, 0.3333, 0.8667, 0.8667],
    "F1-Score": [0.9286, 0.7317, 0.2727, 0.4211, 1.0000, 0.7273, 0.4167, 0.4906, 0.8667]
}

# DataFrame erstellen
df = pd.DataFrame(data)
df.set_index("Label", inplace=True)

# Plot im Stil wie zuvor
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["F1-Score"], 'o-', label="F1-Score")
plt.plot(df.index, df["Precision"], 'o-', label="Precision")
plt.plot(df.index, df["Recall"], 'o-', label="Recall")

# Achsenbeschriftungen im LaTeX-Stil
plt.xlabel(r"$\mathit{Label}$", fontsize=16)
plt.ylabel(r"$\mathit{Wert}$", fontsize=16)

# Achsenticks im 0.2-Schritt für Y-Achse, alle Labels auf X-Achse
plt.yticks(np.arange(0, 1.1, 0.2), fontsize=14)
plt.xticks(fontsize=14)

# Achsenbereich
plt.ylim(0, 1.1)

# Legende und Titel
plt.legend(fontsize=14)

# Gitter
plt.grid(True)

# Layout anpassen
plt.tight_layout()

# Speichern als SVG
plt.savefig("Experiment4_Vergleich_aus_1.svg", format="svg")

# Anzeigen
plt.show()
