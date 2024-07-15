import yt_dlp as youtube_dl
import pafy
import cv2

url = "https://www.youtube.com/watch?v=60h6lpnSgck"
video = pafy.new(url)
# best = video.getbest(preftype="mp4")
best = video.getbest(preftype="webm")

capture = cv2.VideoCapture(best.url)
while True:
    grabbed, frame = capture.read()
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) == ord('q'):
        break