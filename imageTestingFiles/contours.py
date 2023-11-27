import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while True:
    # Read frame from camera capture
    _, frame = vid.read()

    # Convert to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold function, param is tunable
    threshold_param = 150
    ret, thresh = cv2.threshold(img_gray, threshold_param, 255, cv2.THRESH_BINARY)

    # Detect contours
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # Draw contours on original image
    #image_copy= frame.copy()
    #cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0,255,0))

    # Draw contours on blank image
    blank_img = np.zeros((720, 1080, 3), dtype = np.uint8)
    cv2.drawContours(image=blank_img, contours=contours, contourIdx=-1, color=(0,255,0))
    # Show
    cv2.imshow('None contour on black', blank_img)
    #cv2.imshow('None contour', image_copy)
    #cv2.imshow('Threshold binary image', thresh)
    #cv2.imshow('Grayscale Frame', img_gray)
    #cv2.imshow('Color Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 