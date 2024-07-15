import time

from OCVYolo8.OCVMainClass import OCVMainClass
import os
from ultralytics import YOLO
from DBModule.DBCont.DBContPut2DetectTableAsync import DBContPut2DetectTableAsync
import cv2
import math
import asyncio
import datetime
import secrets


class OSVDetect(OCVMainClass):
    logger_name = f"{os.path.basename(__file__)}"
    _weights_dir = "yolo-Weights"
    _weights_file = "yolov8n.pt"
    _data_dir = "data"
    _capture_dir = "capture"
    _model: YOLO = None
    _models_dict: dict = None
    _file_number: int = 0
    _file_name: str = None
    _cap: cv2.VideoCapture = None
    _cap_config: dict = None
    _out = None
    _capture_delay: int = 3
    _cv2 = cv2

    def __init__(self):
        super().__init__()
        self.create_model()
        self.init_cap_res()

    def init_cap_res(self):
        try:
            cap = cv2.VideoCapture(0)
            w, h, fps = (int(cap.get(x)) for x in
                         (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        except Exception as e:
            err_msg = f"{__class__.__name__} can't create cap resource, error: {e}"
            self.logger.error(err_msg)
        else:
            self._cap = cap
            self._cap_config = dict({"height": h, "width": w, "fps": fps})

    def close_cap_res(self):
        self._cap.release()

    def create_model(self):
        model_file = os.path.join(os.path.dirname(__file__), self._weights_dir, self._weights_file)
        self._model = YOLO(model_file)
        self._models_dict = self._model.names
        # print(self._models_dict)

    def change_out_file(self):

        today_date = datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")
        self._file_number += 1
        self._file_name = f"capture_{today_date}_{secrets.token_hex(nbytes=2)}.avi"
        cur_dir = os.path.dirname(__file__)
        record_file_name = os.path.join(cur_dir, self._data_dir, self._capture_dir, self._file_name)
        fps = self._cap_config.get("fps")
        w = self._cap_config.get("width")
        h = self._cap_config.get("height")
        self._out = cv2.VideoWriter(record_file_name, cv2.VideoWriter_fourcc(*"MJPG"), fps, (w, h))

    def img_boxes_handler(self, img, boxes) -> dict:
        detected_classes_names_dict = dict({"person": 0})
        # print(f"{boxes=}")
        for box in boxes:
            cls = int(box.cls[0])
            cls_name = self._models_dict.get(cls)
            detected_classes_names_dict[cls_name] = detected_classes_names_dict.get(cls_name, 0) + 1
            # if cls != 0:
            #     pass
            #     # continue
            # elif cls == 0:
            #     print(f"person detected!!!")
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values
            # confidence
            confidence = math.ceil((box.conf[0] * 100))

            # find only surely confident (>50%)
            if confidence < 50:
                continue

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(img, f"{cls_name} ({confidence}%)", org, font, font_scale, color, thickness)
        return detected_classes_names_dict, img

    def run_detect_from_cap(self):
        """ method capture the frame recognize and writes it in file"""
        person_captured = False
        person_captured_last_time = datetime.datetime.now()
        person_captured_time_delay = self._capture_delay
        try:
            while True:
                # read cap res
                success, img = self._cap.read()
                w = self._cap_config.get("width")
                h = self._cap_config.get("height")

                # run model recognition
                results = self._model(img, imgsz=[w, h], rect=True, verbose=False)
                for result in results:
                    boxes = result.boxes

                    # capture tail part
                    time_limit = person_captured_last_time + datetime.timedelta(seconds=person_captured_time_delay)
                    time_is_passed = datetime.datetime.now() > time_limit
                    # check is person captured during last 3 sec?

                    detected_names_dict, img = self.img_boxes_handler(img, boxes=boxes)
                    persons_num = detected_names_dict.get("person", 0)


                    #if detect person in frame
                    if persons_num > 0:
                        print(f"persons detected {persons_num}")
                        # if first detection
                        if person_captured is False:
                            print(f"person just captured at {datetime.datetime.now()}")
                            self.change_out_file()
                            print(f"video writed in file {self._file_name}")
                            person_captured = True
                            person_captured_last_time = datetime.datetime.now()
                        self._out.write(img)
                    # if person already detected early but not now
                    else:
                        if time_is_passed:
                            if person_captured:
                                person_captured = False
                                person_captured_last_time = datetime.datetime.now()
                                print("capture closed")
                        else:
                            if person_captured:
                                self._out.write(img)

                cv2.imshow('Webcam', img)
                if cv2.waitKey(1) == ord('q'):
                    break

        except Exception as e:
            err_msg = f"{__class__.__name__} can't run detect loop, error: {e}"
            self.logger.error(err_msg)
        finally:
            self.close_cap_res()


if __name__ == '__main__':
    connector = OSVDetect()
    print(connector._models_dict)
    connector.run_detect_from_cap()