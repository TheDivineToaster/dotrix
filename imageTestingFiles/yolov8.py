
import time
import cv2
from PIL import Image
from ultralytics import YOLO

# the algo location
model = YOLO('./train/weights/best.pt')

# define a video capture object
# change if your webcam is the second camera plugged in
vid = cv2.VideoCapture(0)

# modify the framerate if you need a want
frame_rate = 15

prev = 0
while True:

    # checking the frame rate
    time_elapsed = time.time() - prev
    success, frame = vid.read()

    # if the time has elapsed for the framerate then run
    if time_elapsed > 1./frame_rate:
        prev = time.time()

        # if image is captured then process
        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)
            
        # the 'q' button is set as the
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows()