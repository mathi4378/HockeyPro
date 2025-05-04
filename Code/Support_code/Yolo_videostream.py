from ultralytics import YOLO

model = YOLO("E:\\Workspace\\Masterarbeit\\runs\\detect\\train3\\weights\\best.pt")
source = "E:\\Workspace\\Masterarbeit\\Videos\\Test2.mov"

results = model(source,
                show=True,
                conf=0.2,
                iou=0.2)








