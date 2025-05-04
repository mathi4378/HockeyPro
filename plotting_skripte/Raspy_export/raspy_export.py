import matplotlib.pyplot as plt

def plot_Raspy_inference_v2(output_path="raspy_inference.svg"):
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
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # Plot 1: Inferenzzeit
    axes[0].bar(labels, inference, color='blue')
    axes[0].set_xlabel(r"$\mathit{Framework}$", fontsize=16)
    axes[0].set_ylabel(r"$\mathit{Inferenzzeit\ in\ ms/Bild}$", fontsize=16)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].tick_params(axis='both', labelsize=14)

    # Plot 2: mAP50
    axes[1].bar(labels, map50, color='blue')
    axes[1].set_xlabel(r"$\mathit{Framework}$", fontsize=16)
    axes[1].set_ylabel(r"$\mathit{mAP50}$", fontsize=16)
    axes[1].set_ylim(0.607, 0.612)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].tick_params(axis='both', labelsize=14)

    # Layout optimieren
    plt.tight_layout()

    # Speichern als SVG
    plt.savefig(output_path, format="svg")

    # Anzeigen
    plt.show()

# Funktion aufrufen
plot_Raspy_inference_v2("raspy_inference.svg")
