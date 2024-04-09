import cv2
import time
from camera_utils import get_droidcam_url


# Get the URL for the DroidCam server
url = get_droidcam_url()
# Initialize a video capture object with the DroidCam video feed
video = cv2.VideoCapture(url)
# Wait for 1 second to ensure the video capture object is ready
time.sleep(1)
# Initialize variable to store the first frame of the video
first_frame = None

# Infinite loop to continuously capture and display frames from the DroidCam feed
while True:
    # Read a frame from the video capture object
    check, frame = video.read()
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale frame to reduce noise
    gray_frame_gau_blurred = cv2.GaussianBlur(
        gray_frame, (21, 21), 0)

    # Check if it's the first frame. If yes, set the first frame as the current frame
    if first_frame is None:
        first_frame = gray_frame_gau_blurred

    # Compute the absolute difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau_blurred)
    # Threshold the delta frame to create a binary image where motion areas are highlighted
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # Dilate the thresholded image to fill gaps and holes in the detected objects
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Find contours in the dilated image
    contours, check = cv2.findContours(
        dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour
    for contour in contours:
        # Check if the contour area is smaller than 5000 pixels
        if cv2.contourArea(contour) < 5000:
            # If yes, ignore this contour (considered as noise)
            continue
        else:
            # Get the bounding rectangle coordinates
            x, y, w, h = cv2.boundingRect(contour)
            # Draw a green rectangle of width 2 around the detected object on the original frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the original frame with bounding rectangles drawn around detected motion areas in a window titled "Video Captured"
    cv2.imshow("Video Captured", frame)

    # Wait for a key press for 1 millisecond, cv2.waitKey(1) returns ASCII code of key pressed
    key = cv2.waitKey(1)
    # If the 'q' key is pressed, exit the loop, (ord('q') returns ASCII code of 'q'
    if key == ord('q'):
        break

# Release the video capture object
video.release()
# Close all OpenCV windows
cv2.destroyAllWindows()
