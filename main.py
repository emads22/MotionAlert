import cv2
import time
from camera_utils import get_droidcam_url


# Get the URL for the DroidCam server
url = get_droidcam_url()

# Initialize a video capture object with the DroidCam video feed
video = cv2.VideoCapture(url)

# Wait for 1 second to ensure the video capture object is ready
time.sleep(1)

# Infinite loop to continuously capture and display frames from the DroidCam feed
while True:
    # Read a frame from the video capture object
    check, frame = video.read()

    # Display the captured frame in a window titled "my_video"
    cv2.imshow("my_video", frame)

    # Wait for a key press for 1 millisecond, cv2.waitKey(1) returns ASCII code of key pressed
    key = cv2.waitKey(1)

    # If the 'q' key is pressed, exit the loop, (ord('q') returns ASCII code of 'q'
    if key == ord('q'):
        break

# Release the video capture object
video.release()


# Save the captured frame to a file
# cv2.imwrite(output_file, frame)


# Close all OpenCV windows
# cv2.destroyAllWindows()