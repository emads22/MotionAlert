import cv2
import time
from constants import *


def get_droidcam_url():
    """
    Get the URL for the DroidCam server based on environment variables.

    Requires 'DROIDCAM_IP_ADDRESS' and 'DROIDCAM_PORT_NUMBER' environment variables to be set.

    Returns:
    str: The URL for the DroidCam server.
    """
    if not DROIDCAM_IP_ADDRESS or not DROIDCAM_PORT_NUMBER:
        print("\nError: DroidCam IP address or port number not set\n")
        return None

    # Construct the URL for the DroidCam server
    url = f'http://{DROIDCAM_IP_ADDRESS}:{DROIDCAM_PORT_NUMBER}/video'

    return url


def initialize_video_capture(url):
    """
    Initialize a video capture object with the provided URL.

    Parameters:
        url (str): The URL of the video feed.

    Returns:
        cv2.VideoCapture or None: The initialized video capture object if successful, None otherwise.
    """
    try:
        # Attempt to initialize a video capture object with the DroidCam video feed
        video = cv2.VideoCapture(url)
        # Wait for a second to stabilize the feed and ensure the video capture object is ready then return it
        time.sleep(1)
        return video

    except Exception as e:
        # If there's an error opening the feed, print an error message and return None
        print("\nError: Unable to open DroidCam feed\nError: {e}\n")
        return None


def grayscale_and_noise_reduction(frame):
    """
    Converts the provided frame to grayscale and applies Gaussian blur for noise reduction.

    Args:
        frame (numpy.ndarray): The frame to be converted to grayscale.

    Returns:
        numpy.ndarray: The grayscale frame with Gaussian blur applied.
    """
    # Convert the frame to grayscale for motion detection
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale frame to reduce noise
    gray_frame_gau_blurred = cv2.GaussianBlur(
        gray_frame, GAUSSIAN_BLUR_KERNEL_SIZE, 0)

    return gray_frame_gau_blurred


def get_motion_objects_contours(current_frame, first_gray_frame):
    """
    Detects motion objects in the current frame relative to the first frame and returns their contours.

    Args:
        current_frame (numpy.ndarray): The current frame of the video.
        first_gray_frame (numpy.ndarray): The reference frame without motion.

    Returns:
        list of numpy.ndarray: Contours of the motion objects detected in the current frame.
    """
    current_gray_frame = grayscale_and_noise_reduction(current_frame)
    # Calculate the absolute difference between the current frame and the reference frame (first frame)
    delta_frame = cv2.absdiff(first_gray_frame, current_gray_frame)
    # Apply a threshold to obtain the difference as a binary image where motion areas are highlighted
    _, thresh_frame = cv2.threshold(
        delta_frame, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    # Dilate the thresholded image to fill gaps and holes in the detected objects
    dilated_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Find contours of objects in the dilated frame
    contours, _ = cv2.findContours(
        dilated_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def draw_contour_rectangle(frame, contour):
    """
    Draws a rectangle around a detected object in the provided frame based on the given contour.

    Args:
        frame (numpy.ndarray): The original frame where the rectangle will be drawn.
        contour (numpy.ndarray): The contour of the detected object.

    Returns:
        None
    """
    # Get the bounding rectangle coordinates
    x, y, w, h = cv2.boundingRect(contour)
    # Draw a green rectangle of width 2 around the detected object on the original frame
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


def main():
    test_url = get_droidcam_url()
    print(f"\n{test_url}\n")


if __name__ == '__main__':
    main()
