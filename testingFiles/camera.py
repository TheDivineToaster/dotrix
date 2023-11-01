
# import the opencv library 
import cv2
from matplotlib import pyplot as plot


# define a video capture object 
vid = cv2.VideoCapture(1) 

while(True): 

    # Capture the video frame 
    # by frame 
    _, frame = vid.read()

    # Convert to graycsale
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # harr cascade facial recognition
    haarCascade = cv2.CascadeClassifier('./cvAlgos/haarcascade_frontalface_default.xml')

    faceRectangles = haarCascade.detectMultiScale(frameGray, 1.1, 2)

    # draw the facial recognition rectangles for harr cascade
    for (x, y, w, h) in faceRectangles:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    # Blur the image for better edge detection
    frameBlur = cv2.GaussianBlur(frameGray, (1,1), 0) 

    # Canny Edge Detection
    frameEdges = cv2.Canny(image=frameBlur, threshold1=40, threshold2=175) # Canny Edge Detection

    # Display Canny Edge Detection Image
    cv2.imshow('Edges', frameEdges)

    # Display the faces
    cv2.imshow('Faces', frame)

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
