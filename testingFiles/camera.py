
# import the opencv library 
import cv2 


# define a video capture object 
vid = cv2.VideoCapture(1) 

while(True): 

    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    # Convert to graycsale
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (1,1), 0) 

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=40, threshold2=175) # Canny Edge Detection
    
    downscale_edges = cv2.resize(edges, (25,25))

    # Display Canny Edge Detection Image
    cv2.imshow('Canny Output', edges)

        

    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cv2.imwrite("output.jpg", edges)
        cv2.imwrite("output_downscaled.jpg", downscale_edges)
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
