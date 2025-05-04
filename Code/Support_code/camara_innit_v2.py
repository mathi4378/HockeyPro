mport depthai as dai
import cv2 as cv
import numpy as np
import time


def get_calibration(device):
    """Liest die Kamerakalibrierung aus dem Gerät."""
    calibData = device.readCalibration()
    camera_matrix = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RGB, 1280, 720))
    dist_coeffs = np.array(calibData.getDistortionCoefficients(dai.CameraBoardSocket.RGB))
    return camera_matrix, dist_coeffs


def undistort_image(frame, camera_matrix, dist_coeffs):
    """Entzerrt das Bild basierend auf der Kamerakalibrierung."""
    h, w = frame.shape[:2]
    new_camera_matrix, _ = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    undistorted_frame = cv.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)
    return undistorted_frame


def apply_perspective_correction(frame, points):
    """Wendet eine Perspektivenkorrektur basierend auf den vier gewählten Punkten an."""
    h, w = frame.shape[:2]
    src_pts = np.float32(points)
    dst_pts = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv.getPerspectiveTransform(src_pts, dst_pts)
    corrected_frame = cv.warpPerspective(frame, matrix, (w, h))
    return corrected_frame


def crop_image(frame, crop_x, crop_y, crop_w, crop_h):
    """Schneidet das Bild basierend auf den Trackbar-Werten."""
    h, w = frame.shape[:2]
    x_start = min(crop_x, w - 1)
    y_start = min(crop_y, h - 1)
    x_end = min(crop_x + crop_w, w)
    y_end = min(crop_y + crop_h, h)
    return frame[y_start:y_end, x_start:x_end]


def prepare_undistort_and_warp(camera_matrix, dist_coeffs, image_size, points):
    """Berechnet die Maps für Entzerrung und Perspektivkorrektur einmalig."""
    h, w = image_size

    # Neue Kamera-Matrix (optional, kann auch gleich camera_matrix sein)
    new_camera_matrix, _ = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

    # Undistort-Maps vorberechnen
    map1, map2 = cv.initUndistortRectifyMap(
        camera_matrix,
        dist_coeffs,
        None,
        new_camera_matrix,
        (w, h),
        cv.CV_16SC2
    )

    # Perspektiv-Transform vorberechnen
    src_pts = np.float32(points)
    dst_pts = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    perspective_matrix = cv.getPerspectiveTransform(src_pts, dst_pts)

    return map1, map2, perspective_matrix


# def update_crop(val=None):
#    """Aktualisiert die Trackbar-Werte, wenn das Fenster existiert."""
#   if not cv.getWindowProperty("OAK-D Perspektivkorrektur", cv.WND_PROP_VISIBLE):
#      return  # Falls das Fenster nicht existiert, breche die Funktion ab####
#
#   global points, crop_params
#   try:
#      points[0] = (
#     cv.getTrackbarPos("tl_x", "OAK-D Perspektivkorrektur"), cv.getTrackbarPos("tl_y", "OAK-D Perspektivkorrektur"))
#      points[1] = (
#      cv.getTrackbarPos("tr_x", "OAK-D Perspektivkorrektur"), cv.getTrackbarPos("tr_y", "OAK-D Perspektivkorrektur"))
#    points[2] = (
#     cv.getTrackbarPos("bl_x", "OAK-D Perspektivkorrektur"), cv.getTrackbarPos("bl_y", "OAK-D Perspektivkorrektur"))
#     points[3] = (
#    cv.getTrackbarPos("br_x", "OAK-D Perspektivkorrektur"), cv.getTrackbarPos("br_y", "OAK-D Perspektivkorrektur"))
#     cv.createTrackbar("crop_x", "OAK-D Perspektivkorrektur", crop_params[0], 1280, update_crop)
#     cv.createTrackbar("crop_y", "OAK-D Perspektivkorrektur", crop_params[1], 720, update_crop)
#    cv.createTrackbar("crop_w", "OAK-D Perspektivkorrektur", crop_params[2], 1280, update_crop)
#     cv.createTrackbar("crop_h", "OAK-D Perspektivkorrektur", crop_params[3], 720, update_crop)#
#
#    cv.namedWindow("OAK-D Perspektivkorrektur", cv.WINDOW_NORMAL)
#    cv.resizeWindow("OAK-D Perspektivkorrektur", 320, 320)  # Setzt die Fenstergröße auf 400x300 Pixel##

#  except cv.error:
#      pass

points = [(337, 66), (913, 64), (29, 568), (1280, 524)]
# crop_params = [137, 270, 706, 465] #old
crop_params = [100, 280, 800, 440]  # aktuell


def start_camera():
    """Startet die OAK-D Kamera mit Trackbars für Perspektivenkorrektur und Cropping."""
    print("Starte OAK-D Kamera...")
    pipeline = dai.Pipeline()
    colorCam = pipeline.create(dai.node.ColorCamera)
    colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)
    colorCam.setPreviewSize(320, 320)
    colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
    colorCam.setFps(60)
    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("video")
    colorCam.video.link(xout.input)

    try:
        device = dai.Device(pipeline)
        print("Kamera erfolgreich gestartet!")
        queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)
        camera_matrix, dist_coeffs = get_calibration(device)
        # cv.namedWindow("OAK-D Perspektivkorrektur")

        # for label, (x, y) in zip(["tl", "tr", "bl", "br"], points):
        #    cv.createTrackbar(f"{label}_x", "OAK-D Perspektivkorrektur", x, 1280, update_crop)
        #    cv.createTrackbar(f"{label}_y", "OAK-D Perspektivkorrektur", y, 720, update_crop)

        # cv.createTrackbar("crop_x", "OAK-D Perspektivkorrektur", 0, 1280, update_crop)
        # cv.createTrackbar("crop_y", "OAK-D Perspektivkorrektur", 0, 720, update_crop)
        # cv.createTrackbar("crop_w", "OAK-D Perspektivkorrektur", 640, 1280, update_crop)
        # cv.createTrackbar("crop_h", "OAK-D Perspektivkorrektur", 480, 720, update_crop)

        frame_count = 0
        start_time = time.time()  # Startzeit für FPS-Messung

        h, w = 720, 1280  # oder dynamisch vom ersten Frame ablesen
        map1, map2, perspective_matrix = prepare_undistort_and_warp(
            camera_matrix, dist_coeffs, (h, w), points
        )

        while True:
            frame_data = queue.get()
            if frame_data is not None:
                # frame = frame_data.getCvFrame()
                # frame = undistort_image(frame, camera_matrix, dist_coeffs)
                # corrected_frame = apply_perspective_correction(frame, points)
                # cropped_frame = crop_image(corrected_frame, *crop_params)
                # resized_frame = cv.resize(cropped_frame, (320, 320))

                frame = frame_data.getCvFrame()
                # map1, map2, perspective_matrix = prepare_undistort_and_warp(camera_matrix, dist_coeffs, (h, w), points)
                undistorted = cv.remap(frame, map1, map2, interpolation=cv.INTER_LINEAR)
                corrected = cv.warpPerspective(undistorted, perspective_matrix, (w, h))
                cropped = crop_image(corrected, *crop_params)
                resized = cv.resize(cropped, (320, 320))

                # FPS-Berechnung
                frame_count += 1
                elapsed_time = time.time() - start_time

                if elapsed_time > 1.0:  # Alle 1 Sekunde aktualisieren
                    fps = frame_count / elapsed_time
                    print(f"Aktuelle FPS: {fps:.2f}")
                    frame_count = 0
                    start_time = time.time()

                cv.namedWindow("Object detection", cv.WINDOW_NORMAL)
                # cv.imshow("Object detection",resized)

                # print("Höhe (Rows):", corrected_frame.shape[0])
                # print("Breite (Cols):", corrected_frame.shape[1])

                yield resized


    except Exception as e:
        print(f"Fehler beim Starten der Kamera: {e}")
        return None


if __name__ == "__main__":
    start_camera()