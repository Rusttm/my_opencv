import cv2

uri = "https://www.youtube.com/watch?v=60h6lpnSgck"

gst_pipeline = f"uridecodebin uri={uri} ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
# gst_pipeline = "gst-launch-1.0 souphttpsrc is-live=true location=http_youtube_uri ! qtdemux name=demuxer demuxer. ! queue ! h264parse ! nvv4l2decoder ! fakesink" % (uri)

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print('Failed to open source')
    exit(-1)

while True:
    ret, frame = cap.read()
    if not ret:
        print('Failed to read from source')
        break

    cv2.imshow('Test URI', frame)
    cv2.waitKey(1)

cap.release()
