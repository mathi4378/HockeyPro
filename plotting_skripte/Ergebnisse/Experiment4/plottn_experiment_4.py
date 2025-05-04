import matplotlib.pyplot as plt
import pandas as pd

# Metriken vorbereiten
data = {
    "Label": ["A1", "A5", "A9", "C1", "C5", "C9", "E1", "E5", "E9"],
    "Precision": [1.0000, 0.8333, 0.8333, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.7778],
    "Recall": [0.3333, 0.6667, 0.3333, 0.2667, 0.8667, 0.5333, 0.1333, 0.4667, 0.4667],
    "F1-Score": [0.5000, 0.7407, 0.4762, 0.4211, 0.9286, 0.6957, 0.2353, 0.6364, 0.5833]
}

# DataFrame erstellen
df = pd.DataFrame(data)
df.set_index("Label", inplace=True)

# Plot-Stil im YOLO-Design
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["F1-Score"], 'o-', label="F1-Score")
plt.plot(df.index, df["Precision"], 'o-', label="Precision")
plt.plot(df.index, df["Recall"], 'o-', label="Recall")

# Achsenbeschriftungen im LaTeX-Stil
plt.xlabel(r"$\mathit{Label}$", fontsize=16)
plt.ylabel(r"$\mathit{Wert}$", fontsize=16)

# Achsenticks
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Achsenbereich
plt.ylim(0, 1.1)

# Legende und Layout
plt.legend(fontsize=14)
plt.grid(True)
plt.tight_layout()

# Speichern als SVG
plt.savefig("Experiment4_Ergebnis.svg", format="svg")

# Anzeigen
plt.show()
