import os
import pandas as pd
import matplotlib.pyplot as plt
import ast

def plot_hits(input_path, output_path):
    """
    Lädt grouped_hits.csv im input_path, erstellt einen Scatterplot und speichert ihn im output_path als SVG.
    """

    file_path = os.path.join(input_path, "grouped_hits.csv")
    if not os.path.exists(file_path):
        print(f"Datei nicht gefunden: {file_path}")
        return

    os.makedirs(output_path, exist_ok=True)

    # CSV einlesen
    df = pd.read_csv(file_path)

    # Spalte in Tupel umwandeln
    if "Position (x, y) in cm" in df.columns:
        df["Position (x, y) in cm"] = df["Position (x, y) in cm"].apply(ast.literal_eval)
    else:
        print("Spalte 'Position (x, y) in cm' fehlt!")
        return

    # X- und Y-Werte extrahieren
    x_values, y_values = zip(*df["Position (x, y) in cm"].tolist())

    # Plot erstellen
    plt.figure(figsize=(6, 4))
    plt.scatter(x_values, y_values, color='blue', label='Treffer')

    plt.xlabel(r"$\mathit{x\text{-}Position\ in\ cm}$", fontsize=14)
    plt.ylabel(r"$\mathit{y\text{-}Position\ in\ cm}$", fontsize=14)
    plt.xlim(0, 200)
    plt.ylim(0, 120)
    plt.xticks(range(0, 201, 20))
    plt.yticks(range(0, 121, 20))
    plt.grid()
    plt.legend()
    plt.tight_layout()

    # SVG speichern im output_path
    svg_path = os.path.join(output_path, "E7_run3.svg")
    plt.savefig(svg_path, format="svg")

    plt.show()
    plt.close()

    print(f"Plot gespeichert unter: {svg_path}")


# Beispielpfade
input_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment_2_V3\\E7\\Run3"
output_path = "E:\\Workspace\\Masterarbeit\\plotting_skripte\\Diskussion"

plot_hits(input_path, output_path)
