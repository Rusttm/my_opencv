# ! pip install opencv-python
# ! pip install ultralytics

from ultralytics import YOLO

# testing classes
model = YOLO("yolo-Weights/yolov8n.pt")
models_dict = model.names
model_classes = [models_dict[i] for i in range(len(models_dict))]
models_dict.get(28)

# test recognition
import cv2
import math 

# Open the video file
# cap = cv2.VideoCapture("video_store_cam_5min.mp4")
# cap.set(3, 1920)
# cap.set(4, 1024)

# # start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1024)


w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
capture_rec_number = 1
out = cv2.VideoWriter(f"./data/capture/capture_{capture_rec_number}.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))
    

# model
# model = YOLO("yolo-Weights/yolov8n.pt")

while True:
    success, img = cap.read()
    results = model(img, imgsz=[1920, 1080], rect=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # class name
            cls = int(box.cls[0])

            # find only persons
            # if cls > 0:
            #     continue
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # confidence
            confidence = math.ceil((box.conf[0]*100))

            # find only surely confident (>50%)
            # if confidence < 50:
            #     continue
            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 1)

            

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.5
            color = (255, 0, 0)
            thickness = 1

            cv2.putText(img, f"{model_classes[cls]} ({confidence}%)", org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    out.write(img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()