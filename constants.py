from pathlib import Path
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get the IP address and port number of the DroidCam server from environment variables
DROIDCAM_IP_ADDRESS = os.getenv('DROIDCAM_IP_ADDRESS')
DROIDCAM_PORT_NUMBER = os.getenv('DROIDCAM_PORT_NUMBER')

# Constants
MIN_CONTOUR_AREA = 5000
THRESHOLD_VALUE = 60
GAUSSIAN_BLUR_KERNEL_SIZE = (21, 21)
CAPTURED_PICTURES_DIR = Path("./assets") / "captured"
ATTACHED_PICTURES_DIR = Path("./assets") / "attached"

# Email Sending
SENDER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

ASCII_ART = """

███╗   ███╗ ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗       █████╗ ██╗     ███████╗██████╗ ████████╗
████╗ ████║██╔═══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║      ██╔══██╗██║     ██╔════╝██╔══██╗╚══██╔══╝
██╔████╔██║██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║█████╗███████║██║     █████╗  ██████╔╝   ██║   
██║╚██╔╝██║██║   ██║   ██║   ██║██║   ██║██║╚██╗██║╚════╝██╔══██║██║     ██╔══╝  ██╔══██╗   ██║   
██║ ╚═╝ ██║╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║      ██║  ██║███████╗███████╗██║  ██║   ██║   
╚═╝     ╚═╝ ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝      ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   
                                                                                                
"""