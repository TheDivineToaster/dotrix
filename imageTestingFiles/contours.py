import cv2
import numpy as np
import time

vid = cv2.VideoCapture(0)

while True:
    # Read frame from camera capture
    _, frame = vid.read()

    # Convert to grayscale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold function, param is tunable
    threshold_param = 100
    ret, thresh = cv2.threshold(img_gray, threshold_param, 255, cv2.THRESH_BINARY)

    # Detect contours
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # Draw contours on original image
    #image_copy= frame.copy()
    #cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0,255,0))

    # Draw contours on blank image
    all_contours_image = np.zeros((frame.shape[0], frame.shape[1], 3), dtype = np.uint8)
    cv2.drawContours(image=all_contours_image, contours=contours, contourIdx=-1, color=(0,255,0))
    
    # Draw the longest contour on a different blank image
    max_contour_image = np.zeros((frame.shape[0], frame.shape[1], 3), dtype = np.uint8)
    if len(contours) > 1:
        max_contour = max(contours, key = len)
        cv2.drawContours(image=max_contour_image, contours=max_contour, contourIdx=-1, color=(255,255,255))
    
    # Show live feeds (feel free to comment and uncomment with what you need to see)
    cv2.imshow('All contours', all_contours_image)
    cv2.imshow('Just one contour', max_contour_image)
    #cv2.imshow('All contours over image', image_copy)
    #cv2.imshow('Threshold binary image', thresh)
    #cv2.imshow('Grayscale Frame', img_gray)
    #cv2.imshow('Color Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Write original image, image of all contours, image of longest contour
        cv2.imwrite("original_image.png", frame)
        cv2.imwrite("contours.png", all_contours_image)
        cv2.imwrite("longest_contour.png", max_contour_image)
        # Fill in longest contour with white
        timestamp_1 = time.time()
        for i in range(frame.shape[0]):
            for j in range (frame.shape[1]):
                test_val = cv2.pointPolygonTest(max_contour, (j, i), True)
                # If it's in the contour, color it white
                if test_val > 0:
                    max_contour_image[i,j,0] = 255
                    max_contour_image[i,j,1] = 255
                    max_contour_image[i,j,2] = 255
        timestamp_2 = time.time()
        total_time = timestamp_2 - timestamp_1
        print("Filling in contours took " + str(total_time) + " seconds.")
        # Write image of longest contour filled in
        cv2.imwrite("pointPolygonTest.png", max_contour_image)
        
        # Cropping image to a square
        w1 = int(((frame.shape[1] / 2) - (frame.shape[0] / 2)))
        w2 = int(((frame.shape[1] / 2) + (frame.shape[0] / 2)))
        cropped_contour_image = max_contour_image[0:frame.shape[0], w1: w2]
        
        # Downscaling image to 25x25, writing downscaled image
        downscaled_image = cv2.resize(cropped_contour_image, dsize=(25,25), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite("downscaled_image.png", downscaled_image)
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 