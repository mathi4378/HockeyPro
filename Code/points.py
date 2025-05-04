import depthai as dai
import cv2 as cv
import numpy as np

points = []

def get_calibration(device):
    calibData = device.readCalibration()
    camera_matrix = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RGB, 640, 360))
    dist_coeffs = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB))
    return camera_matrix, dist_coeffs

def undistort_image(frame, camera_matrix, dist_coeffs):
    h, w = frame.shape[:2]
    new_camera_matrix, _ = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    return cv.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

# Mausklick-Callback
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Punkt {len(points)}: ({x}, {y})")

# Kamera starten
pipeline = dai.Pipeline()
cam = pipeline.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
cam.setPreviewSize(640, 360)
cam.setFps(60)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("video")
cam.preview.link(xout.input)

with dai.Device(pipeline) as device:
    print("Kamera gestartet. Bitte klicke 4 Punkte: [oben links, oben rechts, unten links, unten rechts]")
    queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)

    # Kalibrierung holen
    camera_matrix, dist_coeffs = get_calibration(device)

    cv.namedWindow("Klick auf 4 Punkte")
    cv.setMouseCallback("Klick auf 4 Punkte", click_event)

    while True:
        in_frame = queue.get()
        frame = in_frame.getCvFrame()

        # >>> Bild entzerren <<<
        undistorted = undistort_image(frame, camera_matrix, dist_coeffs)

        display = undistorted.copy()

        # Zeige bereits gewählte Punkte
        for pt in points:
            cv.circle(display, pt, 5, (0, 255, 0), -1)

        cv.imshow("Klick auf 4 Punkte", display)
        key = cv.waitKey(1)

        if key == ord("q") or len(points) == 4:
            break

    cv.destroyAllWindows()

    if len(points) == 4:
        # Zielpunkte (Ecken des Ausgabebildes 320x320)
        dst_pts = np.array([
            [0, 0],
            [319, 0],
            [0, 319],
            [319, 319]
        ], dtype=np.float32)

        src_pts = np.array(points, dtype=np.float32)
        M = cv.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv.warpPerspective(undistorted, M, (320, 320))

        # Bilder anzeigen
    cv.imshow("Frame 3", warped)
    cv.imshow("Frame 1", frame)
    cv.imshow("Frame 2", undistorted)
    
    # Bilder speichern
    cv.imwrite("frame_original.jpg", frame)
    cv.imwrite("frame_undistorted.jpg", undistorted)
    cv.imwrite("frame_warped.jpg", warped)

    print("Bilder wurden gespeichert als:")
    print(" - frame_original.jpg")
    print(" - frame_undistorted.jpg")
    print(" - frame_warped.jpg")

    cv.waitKey(0)
    cv.destroyAllWindows()

# Punkte zur Wiederverwendung ausgeben
print("\nKopiere folgende Punkte in dein Skript:")
print("points = [")
for pt in points:
    print(f"    (np.float32({pt[0]}), np.float32({pt[1]})),")
print("]")
