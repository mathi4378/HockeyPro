import os
import matplotlib.pyplot as plt
import numpy as np

def plot_separate_experiments(output_dir="E:\\Workspace\\Masterarbeit\\plotting_skripte\\Layouts"):
    os.makedirs(output_dir, exist_ok=True)  # Ordner erstellen, falls nicht vorhanden

    # Punktmengen und zugehörige Labels
    point_sets = [
        {
            "points": [
                (20, 20), (60, 20), (100, 20), (140, 20), (180, 20),
                (20, 60), (60, 60), (100, 60), (140, 60), (180, 60),
                (20, 100), (60, 100), (100, 100), (140, 100), (180, 100)
            ],
            "labels": [
                "A1", "A3", "A5", "A7", "A9",
                "C1", "C3", "C5", "C7", "C9",
                "E1", "E3", "E5", "E7", "E9"
            ],
            "filename": "Experiment1.svg",
            "title": "Experiment 1"
        },
        {
            "points": [
                (40, 20), (100, 20), (160, 20),
                (40, 60), (100, 60), (160, 60),
                (40, 100), (100, 100), (160, 100)
            ],
            "labels": [
                "A2", "A5", "A8",
                "C2", "C5", "C8",
                "E2", "E5", "E8"
            ],
            "filename": "Experiment2.svg",
            "title": "Experiment 2"
        },
        {
            "points": [
                (20, 20), (100, 20), (180, 20),
                (20, 60), (100, 60), (180, 60),
                (20, 100), (100, 100), (180, 100)
            ],
            "labels": [
                "A1", "A5", "A9",
                "C1", "C5", "C9",
                "E1", "E5", "E9"
            ],
            "filename": "Experiment3.svg",
            "title": "Experiment 3"
        },
        {
            "points": [
                (40, 40), (40, 80),
                (160, 40), (160, 80)
            ],
            "labels": [
                "B2", "D2",
                "B8", "D8"
            ],
            "filename": "Experiment4.svg",
            "title": "Experiment 4"
        }
    ]

    for experiment in point_sets:
        x, y = zip(*experiment["points"])
        plt.figure(figsize=(8, 6))
        plt.scatter(x, y, color="tab:blue")

        for i, label in enumerate(experiment["labels"]):
            plt.text(x[i] + 2, y[i], label, fontsize=12)

        # Achsen invertieren (Kamera-Perspektive)
        #plt.gca().invert_yaxis()

        # Achsenbeschriftung
        plt.xlabel(r"$\mathit{x\text{-}Position\ in\ cm}$", fontsize=16)
        plt.ylabel(r"$\mathit{y\text{-}Position\ in\ cm}$", fontsize=16)

        # Achsenticks und Layout
        plt.xticks(np.arange(0, 201, 20), fontsize=14)
        plt.yticks(np.arange(0, 121, 20), fontsize=14)
        plt.grid(True)
        plt.tight_layout()

        # Pfad zusammensetzen und speichern
        save_path = os.path.join(output_dir, experiment["filename"])
        plt.savefig(save_path, format="svg")
        plt.close()

# Funktion aufrufen
plot_separate_experiments()
