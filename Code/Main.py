#importing packages
import pandas as pd
import warnings
import os



# importing functions
from functions import select_input
from signal_process import signal_process
from hit_detection import (
    hit_detection_camera_openvino,
    hit_detection_video_openvino,
    )
from Code.Support_code.Auswertung import (calc_precision,
                                          calc_conf_hits)


#Pfade PC
#video_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment_3\\Calib\\Calib.mp4"  #Pfad zum aktuellen Video
#network_path_openvino = "E:\\Workspace\\Masterarbeit\\runs\\detect\\train5\\weights\\best_openvino_model"
#csv_path = "E:\\Workspace\\Masterarbeit\\Code\\results\\Experiment_3\\Post_Calib"

'''input_path = csv_path
results_path = os.path.join(input_path, "Auswertung")
csv_path_2 = os.path.join(input_path, "grouped_hits.csv") #für Auswertung
conf_matrix_file = os.path.join(results_path, "conf_matrix.txt")
speed_path = os.path.join(input_path, "speed.csv")'''


#Pfade Raspberry Pi
video_path = "//home/anwender/Workspace/Masterarbeit/Code/results/Experiment4/Camera/D5/Video.mp4"
network_path_openvino = "/home/anwender/Workspace/Masterarbeit/runs/detect/train5/weights/best_openvino_model" #yolo11 / 320 / MA_Tor_8"
csv_path = "/home/anwender/Workspace/Masterarbeit/Code/results/Test_18.04"

#Signal processing parameter
method = "sliding_window_threshold"  #sliding_window_threshold
window_size = 3  # Fenstergröße für Filterung
low_threshold = 0.2  # Untere Schwelle für Hysterese
high_threshold = 0.3  # Obere Schwelle für Hysterese


def main():
    # Inferenz
    choice = select_input()  #

    if choice == "1":
        print("Video-Input mit OpenVINO ausgewählt.")
        results_csv_path = os.path.join(csv_path, "raw_hits.csv")
        results = hit_detection_video_openvino(video_path, network_path_openvino, results_csv_path)

    elif choice == "2":
        print("Kamera-Input mit OpenVINO gewählt.")
        results_csv_path = os.path.join(csv_path, "raw_hits.csv")
        results = hit_detection_camera_openvino(network_path_openvino, results_csv_path)

    else:
        print("Ungültige Eingabe")
        return

    print("Verarbeitung abgeschlossen.")

    # Postprocessing
    if os.path.exists(results_csv_path):
        df = pd.read_csv(results_csv_path)

        # Spalten in Listen umwandeln
        hit_data = df["Hit"].tolist()
        timestamps = df["Timestamp (s)"].tolist()
        positions = [
            tuple(map(float, pos.strip("()").split(", "))) if pos != "(None, None)" else (None, None)
            for pos in df["Position (x, y) in cm"]
        ]

        # Signalverarbeitung durchführen
        signal_process(hit_data, timestamps, positions, window_size, low_threshold, high_threshold,csv_path)
    else:
        print(f"Fehler: Die Datei '{results_csv_path}' wurde nicht gefunden.")

    '''
    calc_precision(input_path, true_value, results_path)
    calc_conf_hits(csv_path_2, conf_matrix_file, ground_truth)
    '''


if __name__ == "__main__":
    main()
