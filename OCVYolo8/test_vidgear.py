# youtube stream capture
# from https://github.com/abhiTronix/vidgear
# and https://stackoverflow.com/questions/43032163/how-to-read-youtube-live-stream-using-opencv-python
# $ pip install vidgear
from vidgear.gears import CamGear
import cv2

options = {"STREAM_RESOLUTION": "480p"}
stream = CamGear(source='https://www.youtube.com/watch?v=60h6lpnSgck', stream_mode=True, logging=True, **options).start() # YouTube Video URL as input

# infinite loop
while True:

    frame = stream.read()
    # read frames

    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # do something with frame here

    cv2.imshow("Output Frame", frame)
    # Show output window

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

cv2.destroyAllWindows()
# close output window

# safely close video stream.
stream.stop()