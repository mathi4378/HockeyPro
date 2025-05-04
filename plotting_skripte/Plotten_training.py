import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import matplotlib.pyplot as plt

def plot_training():
    # Daten
    labels = ['Train', 'Validation', 'Test']
    values = [1517, 192, 191]

    # Balkendiagramm erstellen
    plt.bar(labels, values)

    # Achsenbeschriftung (mit größerer Schrift)
    plt.xlabel(r"$\mathit{Datensatz}$", fontsize=16)
    plt.ylabel(r"$\mathit{Anzahl\,der\,Bilder}$", fontsize=16)

    # Achsenticks (Labels auf der Achse) vergrößern
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Layout & Anzeige
    plt.tight_layout()
    plt.show()

    return None



def plot_raspy_inference():
    import matplotlib.pyplot as plt

    # Daten
    labels = [
        "PyTorch", "TorchScript", "ONNX", "OpenVINO", "TF SavedModel",
        "TF GraphDef", "TF Lite", "PaddlePaddle", "MNN", "NCNN"
    ]
    inference = [
        405.238, 526.628, 168.082, 81.192, 377.968,
        487.244, 317.398, 561.892, 112.554, 88.026
    ]

    # Balkendiagramm erstellen
    plt.figure(figsize=(10, 6))
    plt.bar(labels, inference)

    # Achsenbeschriftungen im gewünschten LaTeX-Format
    plt.xlabel(r"$\mathit{Frameworks}$")
    plt.ylabel(r"$\mathit{Inferenzzeit\, (ms)}$")


    # Drehung der x-Achsen-Beschriftungen, damit sie besser lesbar sind
    plt.xticks(rotation=45, ha='right')

    # Diagramm anzeigen
    plt.tight_layout()
    plt.show()

    return None


def plot_Raspy_inference_v2():
    labels = [
        "PyTorch", "TorchScript", "ONNX", "OpenVINO", "TF SavedModel",
        "TF GraphDef", "TF Lite", "PaddlePaddle", "MNN", "NCNN"
    ]
    inference = [
        405.238, 526.628, 168.082, 81.192, 377.968,
        487.244, 317.398, 561.892, 112.554, 88.026
    ]
    map50 = [
        0.6100, 0.6082, 0.6082, 0.6082, 0.6082,
        0.6082, 0.6082, 0.6082, 0.6106, 0.6106
    ]

    # Zwei vertikale Subplots erstellen
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))  # Mehr Höhe für zwei übereinanderliegende Plots

    # Plot 1: Inferenzzeit
    axes[0].bar(labels, inference, color='blue')
    axes[0].set_xlabel(r"$\mathit{Framework}$", fontsize=16)
    axes[0].set_ylabel(r"$\mathit{Inferenzzeit\ in\ ms/Bild}$", fontsize=16)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].tick_params(axis='both', labelsize=14)

    # Plot 2: mAP50
    axes[1].bar(labels, map50, color='blue')
    axes[1].set_xlabel(r"$\mathit{Framework}$", fontsize=16)
    axes[1].set_ylabel(r"$\mathit{mAP50-95}$", fontsize=16)
    axes[1].set_ylim(0.607, 0.612)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='both', labelsize=14)

    # Layout optimieren
    plt.tight_layout()
    plt.show()

    return None

#plot_training()
#plot_raspy_inference()
plot_Raspy_inference_v2()




