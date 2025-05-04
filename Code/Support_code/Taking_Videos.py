import cv2
import time
import os
from camera_innit import start_camera


def record_video(output_path, frame_width, frame_height, fps=70):
    """
    Zeichnet ein Video von der OAK-D Kamera auf und speichert es an einem angegebenen Pfad.

    :param output_path: Dateipfad für das gespeicherte Video (z. B. "output.mp4").
    :param frame_width: Breite der Frames.
    :param frame_height: Höhe der Frames.
    :param fps: Frames pro Sekunde.
    """
    print("Starte Kameraaufnahme...")

    # Sicherstellen, dass der Speicherpfad existiert
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Kamera-Pipeline starten
    camera_feed = start_camera()
    if camera_feed is None:
        print("Fehler: Die Kamera konnte nicht gestartet werden.")
        return

    # VideoWriter initialisieren
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Alternativ 'XVID' falls 'mp4v' Probleme macht
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Prüfen, ob VideoWriter erfolgreich initialisiert wurde
    if not out.isOpened():
        print("Fehler: VideoWriter konnte nicht gestartet werden!")
        return

    start_time = time.time()
    frame_count = 0

    for frame in camera_feed:
        if frame is None:
            print("Warnung: Kein gültiges Frame empfangen!")
            continue

        out.write(frame)

        # Frame anzeigen (optional)
        #cv2.imshow("Kameraaufnahme", frame)
        cv2.namedWindow("Idle Window", cv2.WINDOW_NORMAL)

        # Aufnahme beenden, wenn 'q' gedrückt wird
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Ressourcen freigeben
    out.release()
    cv2.destroyAllWindows()

    duration = time.time() - start_time
    print(f"Aufnahme abgeschlossen. {frame_count} Frames in {duration:.2f} Sekunden aufgezeichnet.")


if __name__ == "__main__":
    frame_width = 320
    frame_height = 320

    output_path = input(
        "Gib den Speicherort für das Video ein (z. B. E:\Workspace\Masterarbeit\Videos\Trial\Test1.mp4 oder /home/admin/workspace/Masterarbeit/Videos_Raspy/25_03/Test1.mp4): ").strip()
    record_video(output_path,frame_width,frame_height)
