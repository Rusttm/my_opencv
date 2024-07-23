# rtsp setup https://kevinsaye.wordpress.com/2018/10/17/making-a-rtsp-server-out-of-a-raspberry-pi-in-15-minutes-or-less/
# after that check $ systemctl status v4l2rtspserver.service
# from https://stackoverflow.com/questions/44901028/opencv-python-rtsp-stream

import cv2
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
# cap = cv2.VideoCapture("rtsp://192.168.1.80:8554/unicast", cv2.CAP_FFMPEG)
cap = cv2.VideoCapture("rtsp://admin:admin@192.168.1.95:1935", cv2.CAP_FFMPEG)

ret, frame = cap.read()
print(f"{ret=}")
while ret:
    cv2.imshow('frame', frame)
    # do other processing on frame...

    ret, frame = cap.read()
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()