# Webcam Monitoring Application

## Overview
Webcam Monitoring Application is a Python script designed to monitor a webcam feed for motion detection, specifically tailored for DroidCam cameras from mobile devices. Users can continuously monitor their DroidCam feed for motion, with the application drawing rectangles around detected motion areas and capturing frames with motion, saving them locally. Additionally, the application sends email notifications with captured images when motion is detected.

If users want to use the laptop camera instead, they can replace the following line:
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

## Installation
1. Clone this repository.
2. Navigate to the repository directory.
3. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the webcam_monitoring.py script:
   ```bash
   python webcam_monitoring.py
   ```
2. Press the 'q' key to exit the application.

## Configuration
You can customize the following settings in the config.py file:
- URL for the webcam feed.
- Minimum contour area for motion detection.
- Threshold value for detecting motion.
- Gaussian blur kernel size for noise reduction.
- Directories for storing captured and attached images.

## Contributing
Contributions are welcome! Here are some ways you can contribute to the project:
- Report bugs and issues
- Suggest new features or improvements
- Submit pull requests with bug fixes or enhancements

## About
This application uses OpenCV for computer vision tasks and provides a simple yet effective solution for webcam monitoring with motion detection.

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the [MIT License](LICENSE).
