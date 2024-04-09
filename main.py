import cv2
import time
from camera_utils import get_droidcam_url, initialize_video_capture
from send_email import send_email


# Constants
MIN_CONTOUR_AREA = 5000
THRESHOLD_VALUE = 60
GAUSSIAN_BLUR_KERNEL_SIZE = (21, 21)


def webcam_monitoring():
    
    url = get_droidcam_url()  # Get the URL for the DroidCam server
    # Initialize a video capture object with the DroidCam video feed
    video = initialize_video_capture(url)

    if video is None:
        return
        
    original_frame_no_rectangles = None  # Initialize variable to store the first frame of the video
    first_frame = None  # Initialize variable to store the first frame in gray of the video
    status_list = []  # List to store the status of motion detection

    # Infinite loop to continuously capture and display frames from the DroidCam feed
    while True:
        
        status = 0  # Default status indicating no motion detected
        check, frame = video.read()  # Read a frame from the video capture object

        if not check:
            # If failed to read a frame, print an error message and release the video object
            print("\nError: Failed to read frame from DroidCam feed\n")
            video.release()
            return
    
        if original_frame_no_rectangles is None:
            # If it's the original frame that has no rectangles (no motions), set it as the reference frame
            original_frame_no_rectangles = frame

        # Convert the frame to grayscale for motion detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to the grayscale frame to reduce noise
        gray_frame_gau_blurred = cv2.GaussianBlur(
            gray_frame, GAUSSIAN_BLUR_KERNEL_SIZE, 0)

        if first_frame is None:
            # If it's the first frame, set it as the reference frame
            first_frame = gray_frame_gau_blurred

        # Calculate the absolute difference between the current frame and the reference frame (first frame)
        delta_frame = cv2.absdiff(first_frame, gray_frame_gau_blurred)
        # Apply a threshold to obtain the difference as a binary image where motion areas are highlighted
        _, thresh_frame = cv2.threshold(delta_frame, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        # Dilate the thresholded image to fill gaps and holes in the detected objects
        dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
        # Find contours of objects in the dilated frame
        contours, _ = cv2.findContours(dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Iterate through the contours
            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                # If the area of contour is smaller than a threshold, ignore it (considered as noise)
                continue
            
            # If a significant contour is found, draw a rectangle around it
            # Get the bounding rectangle coordinates
            x, y, w, h = cv2.boundingRect(contour)
            # Draw a green rectangle of width 2 around the detected object on the original frame and return the modified image
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            
            # Check if the current frame (frame) differs from the first frame (original_frame_no_rectangles) after drawing rectangles.
            if not (frame == original_frame_no_rectangles).all():
                # If this is True, it means that at least one element in the arrays is not equal, indicating that cv2.rectangle() has modified the frame, implying motion detection, so Update the status variable to 1 to indicate motion detection.
                status = 1
                    
        # Append the status to the status list and keep only the last two statuses (also save memory instead of huge list)
        status_list.append(status)
        status_list = status_list[-2:]

        # If the last two statuses indicate a transition from motion to no motion, send an email
        if status_list == [1, 0]:
            send_email()

        print(status_list)  # Print the status list for debugging purposes

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


if __name__ == "__main__":
    webcam_monitoring()
