# from https://pypi.org/project/pafy/
import yt_dlp as youtube_dl
import pafy
import cv2

url = "https://www.youtube.com/watch?v=1fH8WXPcltQ"
video = pafy.new(url)
print("Streams : " + str(video.allstreams))
best = video.getbest(preftype="mp4")
# best = video.getbest(preftype="webm")

print(f"{best.url=}")
smallest = video.videostreams[1]
print(f"{smallest.url=}")
# capture = cv2.VideoCapture(best.url)
capture = cv2.VideoCapture(smallest.url)
if not capture.isOpened():
    print("Cannot open stream")
    exit()
check, frame = capture.read()
print(check, frame)

cv2.imshow('frame', frame)
cv2.waitKey(10)

capture.release()
cv2.destroyAllWindows()