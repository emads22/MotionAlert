import cv2
import time
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def get_droidcam_url():
    """
    Get the URL for the DroidCam server based on environment variables.

    Requires 'DROIDCAM_IP_ADDRESS' and 'DROIDCAM_PORT_NUMBER' environment variables to be set.

    Returns:
    str: The URL for the DroidCam server.
    """
    # Get the IP address and port number of the DroidCam server from environment variables
    droidcam_ip_address = os.getenv('DROIDCAM_IP_ADDRESS')
    droidcam_port_number = os.getenv('DROIDCAM_PORT_NUMBER')

    if not droidcam_ip_address or not droidcam_port_number:
        print("\nError: DroidCam IP address or port number not set\n")
        return None

    # Construct the URL for the DroidCam server
    url = f'http://{droidcam_ip_address}:{droidcam_port_number}/video'

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


def main():
    test_url = get_droidcam_url()
    print(f"\n{test_url}\n")


if __name__ == '__main__':
    main()
