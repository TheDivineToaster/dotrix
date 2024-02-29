
import time
import cv2
from PIL import Image
from ultralytics import YOLO
import torch

# Set device name to 'cuda' or 'gpu' or '0' if PyTorch sees the GPU, not sure which one works but supposedly any should work
# need CUDA capable gpu, cuda installded, cudnn installed, and pytorch installed for the specific version of cuda you are using
torch.cuda.set_device(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# the algo location
model = YOLO('./train/weights/best.pt').to(device)

# define a video capture object
# change if your webcam is the second camera plugged in
vid = cv2.VideoCapture(0)

# modify the framerate if you need a want
frame_rate = 60

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

            # for result boxes find the x and y positions of them
            # then add a circle centered on the box to the frame_circle, a copy of the frame
            frame_circles = frame.copy()
            boxes = results[0].boxes
            for box in boxes:
                x_pos = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
                y_pos = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
                frame_circles = cv2.circle(frame_circles, (x_pos,y_pos), radius=0, color=(255, 255, 255), thickness=4)

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Display the center of the boxes with a little circle 
            cv2.imshow("Center of the Boxes", frame_circles)
            
        # the 'q' button is set as the
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows()