
# import the opencv library 
import cv2
from PIL import Image, ImageFilter, ImageOps
import numpy as np

# globals
resize = False
harr_cascades = False


# define a video capture object 
vid = cv2.VideoCapture(0) 

while(True): 

    # Capture the video frame 
    # by frame 
    _, frame = vid.read()

    # Convert to graycsale
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # harr cascades if that's a direction we want to take with the recognition
    if harr_cascades:
        haarCascade = cv2.CascadeClassifier('./cvAlgos/haarcascade_frontalface_default.xml')

        faceRectangles = haarCascade.detectMultiScale(frameGray, 1.1, 2)

        # draw the harr recognition rectangles for harr cascade
        for (x, y, w, h) in faceRectangles:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


    # Blur the image for better edge detection
    frameBlur = cv2.GaussianBlur(frameGray, ksize=(5,5), sigmaX=0)
    med_val = np.median(frameGray)
    lower = int(max(0 ,0.7*med_val))
    upper = int(min(255,1.3*med_val))

    # playing with pillow, ignore for now unless you wanna change some blurring settings
    #pillowBlur = Image.fromarray(frameBlur)
    #pillowEnhance = pillowBlur.filter(ImageFilter.EDGE_ENHANCE)
    #frameBlurEnhance = np.asarray(pillowEnhance)


    # Canny Edge Detection
    frameEdges = cv2.Canny(image=frameBlur, threshold1=40, threshold2=175) # Canny Edge Detection

    # pillow filtering
    pillowEdges = Image.fromarray(frameEdges)
    if resize:
        imgSmall = pillowEdges.resize((20,20), resample=Image.Resampling.BILINEAR)
        pillowResult = imgSmall.resize(pillowEdges.size, Image.Resampling.NEAREST)
        pillowResult = ImageOps.invert(pillowEdges)
    
    # invert the image by default
    pillowResultInverted = ImageOps.invert(pillowEdges)

    # back to array type for cv2
    frameEdgesFinal = np.asarray(pillowResultInverted)

    # Display Canny Edge Detection Image
    cv2.imshow('Edges Pixelated', frameEdgesFinal)

    # Display the color frame (and harr boxes if used)
    cv2.imshow('Color Frame', frame)

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
