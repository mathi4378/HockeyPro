import matplotlib.pyplot as plt
import numpy as np
import os

def plot_results(results_path):
    conf = [0.1, 0.2, 0.3, 0.4, 0.5]
    std_x = [0.854, 0.854, 0.854, 0.857, 0.875]
    std_y = [0.609, 0.609, 0.609, 0.649, 0.629]


    #Bar Diagram
    x = np.arange(len(conf))  # Positionen der Gruppen
    width = 0.35  # Breite der Balken

    fig, ax = plt.subplots(figsize=(8, 6))
    bars1 = ax.bar(x - width / 2, std_x, width, label=r"$\mathit{Standardabweichung\,in\,x\text{-}Richtung}$")
    bars2 = ax.bar(x + width / 2, std_y, width, label=r"$\mathit{Standardabweichung\,in\,y\text{-}Richtung}$")

    # Achsen & Beschriftungen (LaTeX-Stil)
    ax.set_xlabel(r"$\mathit{Confidence\text{-}Threshold}$")
    ax.set_ylabel(r"$\mathit{Standardabweichung}$")

    ax.set_xticks(x)
    ax.set_xticklabels(conf)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    # Speichern
    svg_path = os.path.join(results_path, "hits_xy_ganz_plot_bar.svg")
    plt.savefig(svg_path, format="svg")

    plt.show()


    #Linien Diagram
    fig, ax = plt.subplots(figsize=(8, 6))

    # Linienplots mit Markern
    ax.plot(conf, std_x, marker='o', linewidth=2, label=r"$\mathit{Standardabweichung\,in\,x\text{-}Richtung}$")
    ax.plot(conf, std_y, marker='s', linewidth=2, label=r"$\mathit{Standardabweichung\,in\,y\text{-}Richtung}$")

    # Achsenbeschriftung im LaTeX-Stil
    ax.set_xlabel(r"$\mathit{Confidence\text{-}Threshold}$", fontsize=12)
    ax.set_ylabel(r"$\mathit{Standardabweichung\,(\mathit{cm})}$", fontsize=12)

    ax.set_xticks(conf)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    plt.tight_layout()

    # Speichern
    svg_path = os.path.join(results_path, "hits_xy_ganz_plot_linie.svg")
    plt.savefig(svg_path, format="svg")
    plt.show()

    return None

def plot_experiment_1():
    import matplotlib.pyplot as plt

    # Definierte Punkte und Labels

    points = [
        (20, 20), (60, 20), (100, 20), (140, 20), (180, 20),
        (20, 60), (60, 60), (100, 60), (140, 60), (180, 60),
        (20, 100), (60, 100), (100, 100), (140, 100), (180, 100)
    ]
    points_2 = [
        (40, 20), (100, 20), (160, 20),
        (40, 60), (100, 60), (160, 60),
        (40, 100), (100, 100), (160, 100),
    ]

    points_3 = [
        (20, 20), (100, 20), (180, 20),
        (20, 60), (100, 60), (180, 60),
        (20, 100), (100, 100), (180, 100),

    ]

    points_4 = [
        (40, 40), (40, 80),
        (160, 40), (160, 80),

    ]

    labels = [
        "A1", "A3", "A5", "A7", "A9",
        "C1", "C3", "C5", "C7", "C9",
        "E1", "E3", "E5", "E7", "E9"
    ]

    labels_2 = [
        "A2", "A5", "A8",
        "C2", "C5", "C8",
        "E2", "E5", "E8"
    ]

    labels_3 = [
        "A1", "A5", "A9",
        "C1",  "C5", "C9",
        "E1", "E5",  "E9"
    ]
    labels_4 = [
        "B2", "D2",
        "B8", "D8"
    ]

    # Aufteilen der Punkte in X- und Y-Koordinaten
    x, y = zip(*points_4)

    # Scatter Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y)
    plt.gca().invert_yaxis()

    # Labels anzeigen
    for i, label in enumerate(labels_4):
        plt.text(x[i] + 2, y[i], label, fontsize=14)

    # Achsenbeschriftung im LaTeX-Stil
    plt.xlabel(r"$\mathit{x\text{-}Position\ in\ cm}$", fontsize=16)
    plt.ylabel(r"$\mathit{y\text{-}Position\ in\ cm}$", fontsize=16)

    # Achsenticks vergrößern
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)



    plt.grid(True)
    plt.gca().invert_yaxis()
    plt.xticks(np.arange(0, 201, 20))
    plt.yticks(np.arange(0, 121, 20))
    plt.tight_layout()
    plt.show()

    return None

input_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment1\\C5\\Yolo11\\Run5"
results_path = os.path.join(input_path, "Auswertung")

#plot_results(results_path)
plot_experiment_1()


