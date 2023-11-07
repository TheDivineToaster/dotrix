
# import the opencv library 
import cv2
from PIL import Image, ImageFilter, ImageOps
import numpy as np


# define a video capture object 
vid = cv2.VideoCapture(0) 

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
    frameBlur = cv2.GaussianBlur(frameGray, ksize=(5,5), sigmaX=0)
    med_val = np.median(frameGray)
    lower = int(max(0 ,0.7*med_val))
    upper = int(min(255,1.3*med_val))
    #pillowBlur = Image.fromarray(frameBlur)
    #pillowEnhance = pillowBlur.filter(ImageFilter.EDGE_ENHANCE)
    #frameBlurEnhance = np.asarray(pillowEnhance)


    # Canny Edge Detection
    frameEdges = cv2.Canny(image=frameBlur, threshold1=40, threshold2=175) # Canny Edge Detection

    # pillow filtering and inversion
    pillowEdges = Image.fromarray(frameEdges)
    imgSmall = pillowEdges.resize((20,20), resample=Image.Resampling.BILINEAR)
    pillowResult = imgSmall.resize(pillowEdges.size, Image.Resampling.NEAREST)
    pillowResult = ImageOps.invert(pillowResult)

    # back to array type for cv2
    frameEdgesPixelate = np.asarray(pillowResult)

    # Display Canny Edge Detection Image
    cv2.imshow('Edges Pixelated', frameEdgesPixelate)

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
