#Quelle : https://medium.com/@sanyagubrani/understanding-confusion-matrix-with-python-76bf1d074408

import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import ast
from scipy.spatial.distance import cdist



def calc_precision(input_path,true_value,results_path):
    #Berechnung der Standardabweichung nach x und y der Hits am selben Punkt

    file_path = os.path.join(input_path, "grouped_hits.csv")
    os.makedirs(results_path, exist_ok=True)

    if not os.path.exists(file_path):
        print(f"Datei {file_path} nicht gefunden")
        return None

    grouped_data = pd.read_csv(file_path)

    if "Position (x, y) in cm" in grouped_data.columns:
        grouped_data["Position (x, y) in cm"] = grouped_data["Position (x, y) in cm"].apply(ast.literal_eval)
    else:
        print("Fehler: 'Position (x, y) in cm' Spalte fehlt!")
        return None

    #x und y Werte aus Tupel extrahieren
    x_values, y_values = zip(*grouped_data["Position (x, y) in cm"].tolist())

    #Mittelwert
    mean_x = np.mean(x_values)
    mean_y = np.mean(y_values)

    #Standardabweichung
    std_x = np.std(x_values)
    std_y = np.std(y_values)

    rsd_x = (std_x / mean_x) * 100
    rsd_y = (std_y / mean_y) * 100

    #True hit
    #true_x, true_y = true_value


    #Mittelwerte als "True values" somit ohne Referenzwert
    true_x = mean_x
    true_y = mean_y

    #Abweichung im Mittel
    deviation_x = mean_x - true_x
    deviation_y = mean_y - true_y

    #Zusammenfassen der Ergebnisse
    result = {
        #"Mittelwert X": mean_x,
        #"Mittelwert Y": mean_y,
        "Standardabweichung X": std_x,
        "Standardabweichung Y": std_y,
        "Relative Standardabweichung X": rsd_x,
        "Relative Standardabweichung Y": rsd_y,
        "Abweichung von True X": deviation_x,
        "Abweichung von True Y": deviation_y
    }

    #Speichern der results als txt
    file_path = os.path.join(results_path, "results.txt")

    with open(file_path, "w") as file:
        file.write("Präzisionsanalyse der Treffer\n")
        file.write("=" * 40 + "\n")

        for key, value in result.items():
            file.write(f"{key}: {value:.3f}\n")
    
    #Plotten der Hits mit x und y mit zoom
    plt.figure(figsize=(6, 4))
    plt.scatter(x_values, y_values, color='red', label='Erkannter Treffer', marker='x' )
    plt.scatter(true_x, true_y, color='green', label='Mittelwert', marker='o')

    for i, (x, y) in enumerate(zip(x_values, y_values), start=1):
        plt.text(x, y, str(i), fontsize=12, ha='right', va='bottom', color='black')

    plt.xlabel(r"$\mathit{x\text{-}Position\,(\mathit{cm})}$")
    plt.ylabel(r"$\mathit{y\text{-}Position\,(\mathit{cm})}$")
    #plt.xlim(0, 200)
    #plt.xticks(range(0, 200, 20))
    #plt.ylim(0, 120)
    plt.legend()
    plt.grid()

    #speichern als Vektorgrafik
    svg_path = os.path.join(results_path, "hits_xy_zoom_plot.svg")
    plt.savefig(svg_path, format="svg")

    plt.show()
    plt.close()
    
    #Plotten der Hits mit x und y ganzes Tor
    plt.figure(figsize=(6, 4))
    plt.scatter(x_values, y_values, color='blue', label='Grouped Hits')
    #plt.scatter(true_x, true_y, color='green', label='Mittelwert', marker='o')

    #for i, (x, y) in enumerate(zip(x_values, y_values), start=1):
    #    plt.text(x, y, str(i), fontsize=12, ha='right', va='bottom', color='black')

    plt.xlabel(r"$\mathit{x\text{-}Position\,(\mathit{cm})}$")
    plt.ylabel(r"$\mathit{y\text{-}Position\,(\mathit{cm})}$")
    plt.xlim(0, 200)
    plt.xticks(range(0, 200, 20))
    plt.ylim(0, 120)
    plt.legend()
    plt.grid()

    # speichern als Vektorgrafik
    svg_path = os.path.join(results_path, "hits_xy_ganz_plot.svg")
    plt.savefig(svg_path, format="svg")

    plt.show()
    plt.close()

    return None

def calc_conf_hits(csv_path, conf_matrix_file, ground_truth):
    os.makedirs(os.path.dirname(conf_matrix_file), exist_ok=True)

    if not os.path.exists(csv_path):
        print(f"Datei {csv_path} nicht gefunden!")
        return

    df = pd.read_csv(csv_path)
    if "Position (x, y) in cm" not in df.columns:
        print("Fehler: Spalte 'Position (x, y) in cm' fehlt!")
        return

    df["Position (x, y) in cm"] = df["Position (x, y) in cm"].apply(ast.literal_eval)
    measured_hits = np.array(df["Position (x, y) in cm"].tolist())
    ground_truth = np.array(ground_truth)

    threshold = 20
    dists = cdist(measured_hits, ground_truth)

    matched_measured = set()
    matched_gt = set()

    for i in range(dists.shape[0]):
        for j in range(dists.shape[1]):
            if dists[i, j] <= threshold and j not in matched_gt and i not in matched_measured:
                matched_measured.add(i)
                matched_gt.add(j)
                break

    tp = len(matched_measured)
    fp = len(measured_hits) - tp
    fn = len(ground_truth) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print(f"True Positives (TP): {tp}")
    print(f"False Positives (FP): {fp}")
    print(f"False Negatives (FN): {fn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1_score:.4f}")

    with open(conf_matrix_file, "w") as f:
        f.write("Konfusionsmatrix-Ergebnisse:\n")
        f.write(f"True Positives (TP): {tp}\n")
        f.write(f"False Positives (FP): {fp}\n")
        f.write(f"False Negatives (FN): {fn}\n\n")
        f.write("Metriken:\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall:    {recall:.4f}\n")
        f.write(f"F1-Score:  {f1_score:.4f}\n")

def calc_inference(speed_path):

    # CSV einlesen
    if not os.path.exists(speed_path):
        print(f"Datei {speed_path} nicht gefunden!")
        return

    df = pd.read_csv(speed_path)


    # Extrahiere Trefferliste
    inference = np.array(df["inference (ms)"].tolist())
    preprocess = np.array(df["preprocess (ms)"].tolist())
    postprocess = np.array(df["postprocess (ms)"].tolist())

    inference_mean = np.mean(inference)
    preprocess_mean = np.mean(preprocess)
    postprocess_mean = np.mean(postprocess)

    # Balkendiagramm erstellen
    x_labels = ['Inference', 'Preprocess', 'Postprocess']
    y_values = [inference_mean, preprocess_mean, postprocess_mean]
    x_pos = np.arange(len(x_labels))

    plt.figure(figsize=(6, 4))
    plt.style.use('_mpl-gallery')

    plt.bar(x_pos, y_values, width=0.5)
    # Achsenbeschriftung
    plt.xticks(x_pos, x_labels)
    plt.ylabel(r"$\mathit{Zeit\,\mathit{(ms)}}$")
    plt.grid

    # Speichern als SVG
    svg_path = os.path.join(results_path, "processing_times.svg")
    plt.savefig(svg_path, format="svg")


    plt.show()
    plt.close()

    return None

#Paths
#input_path = "/home/admin/workspace/Masterarbeit/Code/results/Experiment 2/Run1"
input_path = ("E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment_2_V3\\A9_v2\\Run3")

results_path = os.path.join(input_path, "Auswertung")
csv_path = os.path.join(input_path, "grouped_hits.csv")
conf_matrix_path = os.path.join(results_path, "conf_matrix.txt")
speed_path = os.path.join(input_path, "speed.csv")

#Parameter
true_value = (100,60) #für scatter plot

ground_truth = [
    (180, 100), (180 ,100), (180, 100), (180, 100), (180, 100),
    (180, 100), (180 ,100), (180, 100), (180, 100), (180, 100),
    (180, 100), (180 ,100), (180, 100), (180, 100), (180, 100),
]
'''ground_truth = [
    (100, 20), (100, 20), (100, 20), (100, 20), (100, 20),
    (100, 20), (100, 20), (100, 20), (100, 20), (100, 20),

    (100, 60), (100, 60), (100, 60), (100, 60), (100, 60),
    (100, 60), (100, 60), (100, 60), (100, 60), (100, 60)]'''

#Funktionen aufrufen
calc_precision(input_path,true_value,results_path)
calc_conf_hits(csv_path, conf_matrix_path, ground_truth)

#calc_inference(speed_path)




