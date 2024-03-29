from time import time
from cv2 import VideoCapture
from ultralytics import YOLO
from torch import device
from torch import cuda
from datetime import datetime

class cv_processor:
    
    ## Class initialiation ##
    def __init__(self, model_location: str):
        """Class initialization function

        :param cv_processor self: self
        :param string model_location: a path string that contains the location
        of the pre-trained yolov8 model
        """
        # Set device name to 'cuda' or 'gpu' or '0' if PyTorch sees the GPU, not sure which one works but supposedly any should work
        # need CUDA capable gpu, cuda installded, cudnn installed, and pytorch installed for the specific version of cuda you are using
        self._device = device("cuda" if cuda.is_available() else "cpu")
        
        # the algo location
        self._model= YOLO(model_location).to(self._device)

        # the x and y list of all the hand detections
        # format is [[x1, y1], [x2, y2], ... [xn, yn]]
        # where the x and y is the center of the hands
        self._xy_list= []

        # the video capture from openCV
        self._vid = None
    
    ## getters and setters ##
    def get_xy_list(self):
        """Getter for list of xy values of hand detections

        :param cv_processor self: self
        """
        return self._xy_list
    
    ### class methods ##
    def capture(self):
        """Method to capture any hands in the image
        and save the captured x and y values to the _xy_list
        
        :param cv_processor self: self
        """
        
        # clear old xy_list
        self._xy_list = []
        
        # capture a frame
        success, frame = self._vid.read()

        # TODO make the video frame capture a square so that it corresponds more evenly to the grid of LEDs

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

    def start_cam(self, webcam_num: int):
        """Method that attaches the cv_processor to the webcam so it can use it

        :param cv_processor self: self
        :param int webcam_num: the webcam number
        """
        # define a video capture object
        # change if your webcam is the second camera plugged in
        self._vid = VideoCapture(webcam_num)

    def use_active_cv2_cam(self, cv2_video_capture: VideoCapture):
        """Method that attaches the cv_processor to an opencv capture so it can use it
        This is a way of simply using an ALREADY active opencv feed if needed.

        Use start_cam if nothing else in the program needs to use the webcam.
        This is just a function to use start_cam() if we already have the webcam
        up.

        :param cv_processor self: self
        :param int webcam_num: an already active opencv video feed
        """
        self._vid = cv2_video_capture

    def release(self):
        """Method that releases the video capture object when the processing is done.
        Technically should be done whenever the class is done running.

        ONLY RELEASE IF YOU USED start_cam TO FETCH
        
        YOU WILL LOSE YOUR ACTIVE VideoCapture
        
        DO NOT USE IF YOU USED use_active_cv2_cam()

        :param cv_processor self: self
        """
        # release the video capture object when done 
        self._vid.release()


def main():
    """main function of cv_processor.py for testing"""

    # make a cv_processor object,
    # the directory of the algorithm is passed in
    cv_proc = cv_processor(r"C:\Users\micah\source\repos\dotrix\dotrix\imageTestingFiles\train\weights\best.pt")

    # the camera device number is passed in to attach
    # 0 is first webcam etc
    cv_proc.start_cam(0)

    # modify the framerate if you need a want
    frame_rate = 60
    prev = 0

    # continuous loop
    while True:

        # checking the frame rate
        time_elapsed = time() - prev

        # if the time has elapsed for the framerate then run
        if time_elapsed > 1.0 / frame_rate:
            prev = time()

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