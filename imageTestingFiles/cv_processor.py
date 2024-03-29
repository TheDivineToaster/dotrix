import time
import cv2
from ultralytics import YOLO
import torch
from datetime import datetime

class cv_processor:
    
    def __init__(self, model_location, webcam_num):
        # Set device name to 'cuda' or 'gpu' or '0' if PyTorch sees the GPU, not sure which one works but supposedly any should work
        # need CUDA capable gpu, cuda installded, cudnn installed, and pytorch installed for the specific version of cuda you are using
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # the algo location
        self._model = YOLO(model_location).to(self._device)

        # define a video capture object
        # change if your webcam is the second camera plugged in
        # TODO make the video frame capture a square so that it corresponds more evenly to the grid of LEDs
        self._vid = cv2.VideoCapture(webcam_num)

        self._xy_list = []
    
    # getters and setters
    def get_xy_list(self):
        return self._xy_list
    
    # class methods
    def capture(self):
        
        # clear old xy_list
        self._xy_list = []
        
        # capture a frame
        success, frame = self._vid.read()

        # if image is captured then process
        if success:
            # Run YOLOv8 inference on the frame
            results = self._model(frame)

            # for result boxes find the x and y positions of them
            # the boxes are added to the _xy_list
            # format is [[x1, y1], [x2, y2], ... [xn, yn]]
            # where the x and y is the center of the hands
            boxes = results[0].boxes
            for box in boxes:
                x_pos = int((box.xyxy[0][0] + box.xyxy[0][2]) / 2)
                y_pos = int((box.xyxy[0][1] + box.xyxy[0][3]) / 2)
                self._xy_list.append([x_pos,y_pos])

    def release(self):
        # After the loop release the cap object 
        self._vid.release()


def main():
    """main function of cv_processor.py for testing"""

    # make a cv_processor object,
    # the directory of the algorithm is passed in
    # the camera device number is also passed in
    # 0 is first webcam etc
    cv_proc = cv_processor(r"C:\Users\micah\source\repos\dotrix\dotrix\imageTestingFiles\train\weights\best.pt", 0)

    # modify the framerate if you need a want
    frame_rate = 60
    prev = 0

    # continuous loop
    while True:

        # checking the frame rate
        time_elapsed = time.time() - prev

        # if the time has elapsed for the framerate then run
        if time_elapsed > 1.0 / frame_rate:
            prev = time.time()

            # run a capture of the hands in the frame
            cv_proc.capture()

            # use the getter function to check if there's any
            # items in the the x_y_list from the cv processor
            if cv_proc.get_xy_list():

                # string processing
                box_string = "Boxes: "
                for num, x_y in enumerate(cv_proc.get_xy_list()):
                    box_string += str(num) + ": "
                    for val in x_y:
                        box_string += str(val) + ", "

                # logging the string
                log = open("logfile.txt", "a")
                log.write(datetime.now().strftime("%H:%M:%S") + " "+ box_string + "\n")
                log.close()

if __name__ == "__main__":
    main()