import cv2
import os
import shutil
from threading import Thread
import camera_utils as cu
from send_email import send_email
from constants import *


def clean_directory(directory):
    """
    Clean up the directory by removing all PNG image files.

    Args:
        directory (Path): The directory path from which to remove PNG image files.

    Returns:
        None
    """
    # Get a list of all PNG image files in the directory
    all_img_files = directory.glob("*.png")

    # Iterate over each image file and remove it
    for img_file in all_img_files:
        os.remove(img_file)


def get_motion_object_image():
    """
    Retrieves the image likely to contain the object of interest from the captured images directory,
    copies it to another directory, and returns the path to the copied image.

    The function selects the image that is most likely to contain the object of interest 
    from a sequence of captured images. It finds the middle image in the sequence, as the object 
    of interest is likely to be present in the middle frames of the captured sequence.

    Returns:
        str: The path to the copied image containing the object of interest.
    """
    # Get all saved images in the directory, find the middle index, and select the image in the middle (or closest to the middle)
    # the object of interest is likely to be present in the middle frames of the captured sequence.
    all_images = list(CAPTURED_PICTURES_DIR.glob("*.png"))
    mid_index = len(all_images) // 2
    image_with_object = all_images[mid_index]

    # Copy the image to the destination directory, and save the new path returned from shutil.copy()
    # this way clean_captured_thread wont intervene with email_thread cz the latter will use an image file from outside the captured dir that is being cleared byt the daemon thread clean_aptured_thread
    image_with_object = shutil.copy(
        image_with_object, ATTACHED_PICTURES_DIR)

    return image_with_object


def save_this_frame_locally(frame, id):
    """
    Saves the provided frame as an image file with rectangles indicating motion in a specified directory.

    Args:
        frame (numpy.ndarray): The frame to be saved as an image.
        id (int): The identifier used to generate the filename.

    Returns:
        None
    """
    # Define the output path for the image that has rectangles (with motion) and Write the frame to it as a PNG image
    output_path = CAPTURED_PICTURES_DIR / f"image_{id}.png"
    cv2.imwrite(str(output_path), frame)


def webcam_monitoring():

    url = cu.get_droidcam_url()  # Get the URL for the DroidCam server
    # Initialize a video capture object with the DroidCam video feed
    video = cu.initialize_video_capture(url)

    if video is None:
        return

    # Initialize variable to store the first frame of the video
    original_frame_no_rectangles = None
    # Initialize variable to store the first frame in gray of the video
    first_gray_frame = None
    status_list = []  # List to store the status of motion detection
    img_id = 1  # Counter to keep track of image IDs

    # Infinite loop to continuously capture and display frames from the DroidCam feed
    while True:

        status = 0  # Default status indicating no motion detected
        check, frame = video.read()  # Read a frame from the video capture object

        if not check:
            print("\nError: Failed to read frame from DroidCam feed\n")
            return  # Exit the function if failed to read frame

        if original_frame_no_rectangles is None:
            # If it's the original frame that has no rectangles (no motions), set it as the reference frame
            original_frame_no_rectangles = frame

        if first_gray_frame is None:
            # If it's the first frame, Convert the current frame to grayscale and set it as the reference gray frame for motion detection and skip this iteration to the next one
            first_gray_frame = cu.grayscale_and_noise_reduction(frame)
            continue

        # Get contours of motion objects in the current frame relative to the first frame
        contours = cu.get_motion_objects_contours(frame, first_gray_frame)

        # Iterate through the contours
        for contour in contours:
            # If a contour is found with an area that is higher than a threshold draw rectangle, otherwise ignore it (considered as noise)
            if cv2.contourArea(contour) > cu.MIN_CONTOUR_AREA:
                # Draw a rectangle around the detected object on the frame
                cu.draw_contour_rectangle(frame, contour)

                # Check if the current frame (frame) differs from the first frame (original_frame_no_rectangles) after drawing rectangles.
                if not (frame == original_frame_no_rectangles).all():
                    # If this is True, it indicates that cv2.rectangle() has modified the frame, implying that motion has been detected. Therefore, update the status variable to 1 to indicate motion detection.
                    status = 1

                    # Save the current frame locally as an image with rectangles indicating motion
                    save_this_frame_locally(frame, img_id)
                    img_id += 1  # Increment the image ID for the next image

        # Append the status to the status list and keep only the last two statuses (also save memory instead of huge list)
        status_list.append(status)
        status_list = status_list[-2:]

        # If the last two statuses indicate a transition from motion to no motion, send an email
        if status_list == [1, 0]:
            # Retrieve the image likely to contain the object in motion
            motion_object_picture = get_motion_object_image()

            # Create a thread for sending the email with the captured image (daemon thread to ensure it doesn't prevent program termination)
            email_thread = Thread(target=send_email, args=(
                motion_object_picture,), daemon=True)

            # Create a thread for cleaning up the captured directory (daemon thread to ensure it doesn't prevent program termination)
            clean_captured_thread = Thread(target=clean_directory, args=(
                CAPTURED_PICTURES_DIR,), daemon=True)

            # Start the email_thread to send the email asynchronously.
            email_thread.start()
            # Start the clean_captured_thread to clear the captured directory asynchronously.
            clean_captured_thread.start()

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

    # finally clean the attached directory
    clean_directory(ATTACHED_PICTURES_DIR)

    # Ensure the email is sent before the program exits by waiting for the email thread to finish, but only attempt to join the thread if it exists
    if email_thread:
        email_thread.join()


if __name__ == "__main__":
    webcam_monitoring()
