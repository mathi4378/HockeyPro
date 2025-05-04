import matplotlib.pyplot as plt

def plot_training(output_path="training_dataset_distribution.svg"):
    # Daten
    labels = ['Train', 'Validation', 'Test']
    values = [1517, 192, 191]

    # Balkendiagramm erstellen
    plt.figure(figsize=(6, 5))
    plt.bar(labels, values, color='tab:blue')

    # Achsenbeschriftung (mit größerer Schrift)
    plt.xlabel(r"$\mathit{Datensatz}$", fontsize=16)
    plt.ylabel(r"$\mathit{Anzahl\,der\,Bilder}$", fontsize=16)

    # Achsenticks (Labels auf der Achse) vergrößern
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Layout optimieren
    plt.tight_layout()

    # Speichern als SVG
    plt.savefig(output_path, format="svg")

    # Anzeigen
    plt.show()

# Aufruf
plot_training("training_dataset_distribution.svg")
