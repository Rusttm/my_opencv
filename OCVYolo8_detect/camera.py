# test webcam
import cv2

cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1024)

while True:
    ret, img = cap.read()
    cv2.imshow('Webcam', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()