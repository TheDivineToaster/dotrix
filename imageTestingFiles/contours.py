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
    image_copy= frame.copy()
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0,255,0))

    # Draw contours on blank image
    blank_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype = np.uint8)
    cv2.drawContours(image=blank_img, contours=contours, contourIdx=-1, color=(0,255,0))

    # Show
    cv2.imshow('None contour on black', blank_img)
    #cv2.imshow('None contour', image_copy)
    #cv2.imshow('Threshold binary image', thresh)
    #cv2.imshow('Grayscale Frame', img_gray)
    #cv2.imshow('Color Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        for i in range(frame.shape[0]):
            for j in range (frame.shape[1]):
                test_val = cv2.pointPolygonTest(contours[0], (j, i), True)
                if test_val > 0:
                    blank_img[i,j,0] = 255
                    blank_img[i,j,1] = 255
                    blank_img[i,j,2] = 255
                elif test_val < 0:
                    blank_img[i,j,0] = 0
                    blank_img[i,j,1] = 0
                    blank_img[i,1,2] = 0
                elif test_val == 0:
                    blank_img[i,j,0] = 0
                    blank_img[i,j,1] = 255
                    blank_img[i,j,2] = 0
        #cv2.imwrite("contours.png", blank_img_copy)
        cv2.imwrite("pointPolygonTest.png", blank_img)
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 