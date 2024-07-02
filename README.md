# MotionAlert

## Overview
MotionAlert is a Python application designed to monitor a webcam feed for motion detection using either a computer camera or any IP camera (also known as a network camera). It is a CLI application that keeps running to detect motion, and whenever the `Q` button (the 'q' key) is pressed, the program exits. This logic can be improved for daily use or real-life applications to avoid the need for human interaction to press anything. When motion is detected, the application sends an email notification with an image attachment of the detected motion.

To demonstrate its functionality, this application specifically uses the DroidCam app as a server.

## Features
- **Motion Detection**: Detects motion in the webcam feed using computer vision techniques.
- **Email Notification**: Sends an email notification with an attached image when motion is detected.
- **Automated Cleanup**: Cleans up captured images directory after sending an email notification.

## Technologies Used
- **numpy**: For numerical operations and handling arrays.
- **opencv-python**: For computer vision tasks and processing the webcam feed.
- **pillow**: For image processing and manipulation.
- **python-dotenv**: For managing environment variables.
- **threading**: For running multiple threads concurrently.

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Configure the necessary parameters such as `DROIDCAM_IP_ADDRESS`, `DROIDCAM_PORT_NUMBER`, `USER`, `PASSWORD`, and `RECEIVER` in `constants.py` file.
   - Make sure to provide valid SMTP credentials for sending emails.
5. Run the script using `python webcam_monitoring.py`.

## Usage
1. Run the script using `python webcam_monitoring.py`.
2. Ensure the DroidCam app is running and providing a video feed.
3. Monitor the terminal for status updates and debug messages.
4. When motion is detected, an email notification will be sent with an attached image of the detected motion.

## Using Laptop Camera
If users want to use the laptop camera instead of DroidCam, they can replace the following lines:

```python
url = cu.get_droidcam_url()  # Get the URL for the DroidCam server
video = cu.initialize_video_capture(url)  # Initialize a video capture object with the DroidCam video feed
```

with:

```python
video = cv2.VideoCapture(0)  # Use the default laptop camera (index 0)
# or
video = cv2.VideoCapture(1)  # Use the second available camera (index 1), depending on preference
```

## OpenCV and Motion Detection Logic
The motion detection in this project follows a simple logic:
1. **Background Subtraction**: It starts with background subtraction by converting frames to grayscale and then applying Gaussian blur for noise reduction.
2. **Motion Detection**: It calculates the absolute difference between the current frame and the reference frame to identify motion areas.
3. **Contour Detection**: It finds contours of objects in the difference frame and draws rectangles around them.
4. **Email Notification**: When motion is detected, an email notification is sent with an attached image of the detected motion.

## Automated Cleanup
After sending an email notification, the captured images directory is automatically cleaned up to remove all PNG image files.

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.