from ultralytics import YOLO

model = YOLO("yolo-Weights/yolov8x.pt")
source = "https://youtu.be/1Sj-UdjqlFw"
results = model.predict(source, stream=True)

for r in results:
    next(results)