import matplotlib.pyplot as plt

# Konfidenzwerte
conf = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

# Daten strukturieren




import matplotlib.pyplot as plt

def plot_group(prefix):
    fig = plt.figure(figsize=(8, 16))  # Größe des gesamten Figures
    gs = fig.add_gridspec(5, 1)         # 3 Zeilen, 2 Spalten

    # Manuell gewählte Positionen für 5 Subplots
    positions = [
        (0, 0),  # Zeile 1, links
        (1, 0),  # Zeile 1, rechts
        (2, 0),  # Zeile 2, links
        (3, 0),  # Zeile 2, rechts
        (4, 0)   # Zeile 3, rechts → ergibt zentrierte Optik
    ]

    for idx, suffix in enumerate(['1', '3', '5', '7', '9']):
        row, col = positions[idx]
        ax = fig.add_subplot(gs[row, col])

        key = prefix + suffix
        ax.plot(conf, data[key]['f1'], label='F1-Score', marker='o')
        ax.plot(conf, data[key]['prec'], label='Precision', marker='x')
        ax.plot(conf, data[key]['rec'], label='Recall', marker='s')

        ax.set_title(f'{key}', fontsize=16)
        ax.set_xlabel("Confidence", fontsize=16)
        ax.set_ylim(0, 1.1)
        ax.grid(True)
        ax.tick_params(axis='both', labelsize=14)

        # Linke Spalte oder unterer Plot → Y-Achsenbeschriftung
        if col == 0 or idx == 4:
            ax.set_ylabel("Score", fontsize=16)

        # Letzter Plot → Legende
        if idx == 4:
            ax.legend(loc='lower right', fontsize=16)

    plt.tight_layout()
    plt.show()


def plot_all_groups_vertical():
    groups = ['A', 'C', 'E']
    suffixes = ['1', '3', '5', '7', '9']

    fig, axes = plt.subplots(5, 3, figsize=(18, 18), sharex=True, sharey=True)

    for col, group in enumerate(groups):
        for row, suffix in enumerate(suffixes):
            key = group + suffix
            ax = axes[row, col]

            ax.plot(conf, data[key]['f1'], label='F1-Score', marker='o')
            ax.plot(conf, data[key]['prec'], label='Precision', marker='x')
            ax.plot(conf, data[key]['rec'], label='Recall', marker='s')

            ax.set_title(f'{key}', fontsize=13)
            ax.set_ylim(0, 1.1)
            ax.grid(True)
            ax.tick_params(axis='both', labelsize=11)

            if col == 0:
                ax.set_ylabel("Score", fontsize=12)
            if row == 4:
                ax.set_xlabel("Confidence", fontsize=12)
            if row == 4 and col == 2:
                ax.legend(loc='lower right', fontsize=10)

    plt.tight_layout()
    plt.show()

# Plots für Gruppen A, C, E
plot_group('A')
plot_group('C')
plot_group('E')
plot_all_groups_vertical()