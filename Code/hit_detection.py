import ultralytics
import cv2 as cv
import time
import pandas as pd
import os

#Importieren der Funktionen
from camera_innit import start_camera

def hit_detection_video_openvino(video_path,
                                 network_path_openvino,
                                 results_csv_path):
    # Laden des YOLO-Modells
    print("Lade YOLO OpenVINO-Modell...")
    try:
        model = ultralytics.YOLO(network_path_openvino)
        print("Modell erfolgreich geladen!")
    except Exception as e:
        print(f"Fehler beim Laden des YOLO-Modells: {e}")
        return

    # Öffnen der Videodatei
    print("Öffne Videodatei...")
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print("Fehler: Video konnte nicht geöffnet werden.")
        return

    # Listen zur Speicherung der Erkennungs- und Geschwindigkeitsdaten
    results_data = []
    speed_data = []
    frame_count = 0

    # Pfad für die separate CSV-Datei mit Zeitmessungen
    speed_csv_path = os.path.join(os.path.dirname(results_csv_path), "speed.csv")

    success, first_frame = cap.read()
    if not success:
        print("Fehler: Erstes Frame konnte nicht gelesen werden.")
        cap.release()
        return

    print("Starte Verarbeitung des Videos...")
    try:
        while cap.isOpened():
            # Lesen des nächsten Frames
            success, frame = cap.read()
            if not success:
                print("Videoverarbeitung abgeschlossen.")
                break

            # Zeitstempel des aktuellen Frames
            frame_timestamp = cap.get(cv.CAP_PROP_POS_MSEC) / 1000

            # Inferenz mit dem YOLO-Modell durchführen
            results = model(
                frame,
                show=False,
                imgsz=320,
                conf=0.3,
                iou=0.3
            )

            # Extrahieren der Verarbeitungszeiten aus dem YOLO-Modell
            infer_time_ms = results[0].speed["inference"]
            preprocess_time_ms = results[0].speed["preprocess"]
            postprocess_time_ms = results[0].speed["postprocess"]

            # Speichern der Geschwindigkeitsdaten für den aktuellen Frame
            speed_data.append({
                "frame": frame_count,
                "timestamp (s)": frame_timestamp,
                "inference (ms)": infer_time_ms,
                "preprocess (ms)": preprocess_time_ms,
                "postprocess (ms)": postprocess_time_ms
            })

            hit_positions = [] # Liste zur Speicherung der Trefferkoordinaten

            # Auswertung der Erkennungsergebnisse
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        x, y, w, h = box.xywhn[0]

                        # Offset aus der Kalibrierung
                        x_offset = -2.505
                        y_offset = 0.305

                        # Umrechnung von normierten Koordinaten in Zentimeter
                        x_cm = round(200 - x.item() * 200 + x_offset, 2)
                        y_cm = round(120 - y.item() * 120 + y_offset, 2)

                        hit_positions.append((x_cm, y_cm))

            # Ergebnisse speichern – je nachdem, ob Treffer erkannt wurden oder nicht
            if not hit_positions:
                results_data.append({
                    "Hit": 0,
                    "Position (x, y) in cm": (None, None),
                    "Timestamp (s)": frame_timestamp
                })
            else:
                for position in hit_positions:
                    results_data.append({
                        "Hit": 1,
                        "Position (x, y) in cm": position,
                        "Timestamp (s)": frame_timestamp
                    })

            frame_count += 1

            # Möglichkeit, das Programm per Tastendruck 'q' vorzeitig zu beenden
            if cv.waitKey(1) == ord('q'):
                print("\nVerarbeitung manuell mit 'q' beendet.")
                break

    # Fehlerbehandlung für die Videoverarbeitung
    except Exception as e:
        print(f"Fehler während der Verarbeitung: {e}")

    # Ressourcen und Fenster freigeben
    cap.release()
    cv.destroyAllWindows()

    # Speichern der Erkennungsdaten in CSV-Datei
    pd.DataFrame(results_data).to_csv(results_csv_path, index=False)
    print(f"Ergebnisse gespeichert unter: {results_csv_path}")

    # Speichern der Inferenzzeiten in separater CSV-Datei
    pd.DataFrame(speed_data).to_csv(speed_csv_path, index=False)
    print(f"Speed-Daten gespeichert unter: {speed_csv_path}")

    # Rückgabe der Trefferergebnisse
    return results_data



def hit_detection_camera_openvino(network_path_openvino,
                                  results_csv_path):
    # Start des Kamera-Feeds
    print("Starte Kamera-Feed...")
    camera_feed = start_camera()

    # Laden des YOLO-Modells
    print("Lade YOLO OpenVINO-Modell...")
    try:
        model = ultralytics.YOLO(network_path_openvino)
        print("Modell erfolgreich geladen!")
    except Exception as e:
        print(f"Fehler beim Laden des YOLO-Modells: {e}")
        return

    # Liste zur Speicherung der Ergebnisdaten
    results_data = []
    start_time = time.time()  # Startzeit zur Berechnung der Zeitstempel
    frame_count = 0  # Zähler für verarbeitete Frames (optional erweiterbar)

    try:
        while True:
            # Nächstes Bild von der Kamera holen
            frame = next(camera_feed)

            # Falls kein gültiges Bild empfangen wurde, nächsten Frame abwarten
            if frame is None or frame.size == 0:
                print("Warnung: Leerer Frame empfangen. Warte auf ein neues Bild...")
                continue

            # Inferenz mit dem YOLO-Modell durchführen
            results = model(
                frame,
                show=False,
                imgsz=320,
                conf=0.3,
                iou=0.3
            )

            hit_positions = []  # Liste zur Speicherung der Trefferkoordinaten

            # Auswertung der Erkennungsergebnisse
            for result in results:
                if result.boxes:
                    for box in result.boxes:
                        # Normalisierte Bounding Box-Koordinaten extrahieren
                        x, y, w, h = box.xywhn[0]

                        # Offsets aus der Kalibrierung
                        x_offset = 2.5    # in cm
                        y_offset = -0.55  # in cm

                        # Umrechnung von normierten Koordinaten in Zentimeter
                        x_cm = round(200 - x.item() * 200 + x_offset, 2)
                        y_cm = round(120 - y.item() * 120 + y_offset, 2)

                        hit_positions.append((x_cm, y_cm))

            # Zeitstempel für den aktuellen Frame berechnen
            timestamp = time.time() - start_time

            # Ergebnisse speichern – je nachdem, ob Treffer erkannt wurden oder nicht
            if not hit_positions:
                results_data.append({
                    "Hit": 0,
                    "Position (x, y) in cm": (None, None),
                    "Timestamp (s)": timestamp
                })
            else:
                for position in hit_positions:
                    results_data.append({
                        "Hit": 1,
                        "Position (x, y) in cm": position,
                        "Timestamp (s)": timestamp
                    })

            # Manuelles Beenden über die Taste 'q'
            if cv.waitKey(1) == ord('q'):
                print("\nAufnahme manuell mit 'q' beendet.")
                break

    # Fehlerbehandlung für die Live-Aufnahme
    except Exception as e:
        print(f"Fehler während der Aufnahme: {e}")

    # Fenster und Ressourcen freigeben
    cv.destroyAllWindows()

    # Speichern der Ergebnisse als CSV-Datei
    pd.DataFrame(results_data).to_csv(results_csv_path, index=False)
    print(f"Ergebnisse gespeichert unter: {results_csv_path}")

    # Rückgabe der Ergebnisse
    return results_data


