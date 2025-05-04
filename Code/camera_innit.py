import depthai as dai
import cv2 as cv
import numpy as np
import time

def get_calibration(device):
    calibData = device.readCalibration()
    camera_matrix = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RGB, 640, 360))
    dist_coeffs = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB))
    return camera_matrix, dist_coeffs


#Falls nötig wieder auskommentieren
def undistort_image(frame, camera_matrix, dist_coeffs, new_camera_matrix):
    return cv.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    
#Punkte aus dem points-Skript
points = [
    (np.float32(167), np.float32(91)),
    (np.float32(394), np.float32(92)),
    (np.float32(75), np.float32(249)),
    (np.float32(465), np.float32(242)),
]

def start_camera():
    print("Starte OAK-D Kamera...")
    pipeline = dai.Pipeline()
    colorCam = pipeline.create(dai.node.ColorCamera)
    colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)

    #Kameraparameter setzen
    colorCam.setPreviewSize(640, 360)
    colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
    colorCam.setFps(70)

    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("video")
    colorCam.preview.link(xout.input)

    try:
        device = dai.Device(pipeline)
        print("Kamera erfolgreich gestartet!")
        queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)
        camera_matrix, dist_coeffs = get_calibration(device) #auslesen der Kameradaten

        new_camera_matrix, _ = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (640, 360), 1, (640, 360))

        frame_count = 0
        start_time = time.time()

        while True:
            frame_data = queue.get()
            if frame_data is not None:
                frame = frame_data.getCvFrame()

                #Entzerrung des Bildes
                undistorted = undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix) #hier falls nötig wieder Funktion von oben einfügen, sollte aber so auch funktionieren

                if len(points) == 4:
                    dst_pts = np.array([
                        [0, 0],
                        [319, 0],
                        [0, 319],
                        [319, 319]
                    ], dtype=np.float32)

                    src_pts = np.array(points, dtype=np.float32)
                    M = cv.getPerspectiveTransform(src_pts, dst_pts)
                    output_frame = cv.warpPerspective(undistorted, M, (320, 320))
               

                # FPS-Anzeige
                frame_count += 1
                elapsed_time = time.time() - start_time
                if elapsed_time > 1.0:
                    fps = frame_count / elapsed_time
                    print(f"Aktuelle FPS: {fps:.2f}")
                    frame_count = 0
                    start_time = time.time()

                #Idle Window zum Schließen der Aufnahme
                cv.namedWindow("Idle Window", cv.WINDOW_NORMAL)
                #cv.namedWindow("frame", frame)

                if cv.waitKey(1) == ord("q"):
                    break

                yield output_frame

    except Exception as e:
        print(f"Fehler beim Starten der Kamera: {e}")
