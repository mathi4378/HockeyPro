import depthai as dai
import cv2 as cv
import numpy as np

# Liste zur Speicherung der geklickten Punkte
points = []


# Holt die Kalibrierdaten der RGB-Kamera (Kameramatrix und Verzerrungskoeffizienten)
def get_calibration(device):
    calibData = device.readCalibration()
    camera_matrix = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RGB, 640, 360))
    dist_coeffs = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB))
    return camera_matrix, dist_coeffs


# Entzerrt ein Bild basierend auf der Kamerakalibrierung
def undistort_image(frame, camera_matrix, dist_coeffs):
    h, w = frame.shape[:2]
    new_camera_matrix, _ = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    return cv.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)


# Callback-Funktion für Mausklicks – speichert maximal 4 Punkte
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Punkt {len(points)}: ({x}, {y})")


# DepthAI-Pipeline aufsetzen
pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
cam.setPreviewSize(640, 360)
cam.setFps(60)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("video")
cam.preview.link(xout.input)

# Gerät starten und Kamera-Stream empfangen
with dai.Device(pipeline) as device:
    print("Kamera gestartet. Bitte klicke 4 Punkte: [oben links, oben rechts, unten links, unten rechts]")
    queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Kalibrierdaten laden
    camera_matrix, dist_coeffs = get_calibration(device)

    # Fenster und Mausklick-Funktion setzen
    cv.namedWindow("Klick auf 4 Punkte")
    cv.setMouseCallback("Klick auf 4 Punkte", click_event)

    while True:
        # Aktuelles Frame holen
        in_frame = queue.get()
        frame = in_frame.getCvFrame()

        # Bild entzerren
        undistorted = undistort_image(frame, camera_matrix, dist_coeffs)
        display = undistorted.copy()

        # Bereits gewählte Punkte einzeichnen
        for pt in points:
            cv.circle(display, pt, 5, (0, 255, 0), -1)

        # Anzeige
        cv.imshow("Klick auf 4 Punkte", display)
        key = cv.waitKey(1)

        # Beenden mit 'q' oder nach Auswahl von 4 Punkten
        if key == ord("q") or len(points) == 4:
            break

    cv.destroyAllWindows()

    # Nach 4 Punkten: Perspektivtransformation auf 320x320 anwenden
    if len(points) == 4:
        # Zielpunkte im Ausgabebild
        dst_pts = np.array([
            [0, 0],
            [319, 0],
            [0, 319],
            [319, 319]
        ], dtype=np.float32)

        src_pts = np.array(points, dtype=np.float32)
        M = cv.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv.warpPerspective(undistorted, M, (320, 320))

        # Zeige entzerrtes, transformiertes Bild
        cv.imshow("Gestrecktes Bild (320x320)", warped)
        cv.waitKey(0)
        cv.destroyAllWindows()

# Export der Punkte zur Wiederverwendung
print("\nKopiere folgende Punkte in dein Skript:")
print("points = [")
for pt in points:
    print(f"    (np.float32({pt[0]}), np.float32({pt[1]})),")
print("]")
