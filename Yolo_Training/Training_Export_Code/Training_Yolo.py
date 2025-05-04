from ultralytics import YOLO
from roboflow import Roboflow
import os

rf = Roboflow(api_key="f2IufEsSWDqrR1xvQjL7")
project = rf.workspace("masterarbeit-d3zse").project("ma_tor")
version = project.version(8)
dataset = version.download("yolov8")

# Define paths for data and model
data_yaml_path = "E:\\Workspace\\Masterarbeit\\Yolo_Training\\Training_Export_Code\\MA_Tor-8\\data.yaml"  # Update if the path differs

# Load a model
model = YOLO("E:\\Workspace\\Masterarbeit\\Yolo_Training\\yolov8n.pt")

#Train the model
train_results = model.train(
    data=data_yaml_path,  # path to dataset YAML
    epochs=1000,  # number of training epochs
    imgsz=320,  # training image size
    device="cpu",
    patience=30
    )
