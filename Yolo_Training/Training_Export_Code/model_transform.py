from ultralytics import YOLO

model = YOLO("E:\\Workspace\\Masterarbeit\\runs\\detect\\train5\\weights\\best.pt")  # load a custom trained model

model.export(format="openvino",
             imgsz = 320,
             half=True,
             nms=False
             )