import cv2
from cap_from_youtube import cap_from_youtube

youtube_url = 'https://www.youtube.com/watch?v=60h6lpnSgck'
cap = cap_from_youtube(youtube_url, '480p')

cv2.namedWindow('video', cv2.WINDOW_NORMAL)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break