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


def main():
    test_url = get_droidcam_url()
    print(f"\n{test_url}\n")

if __name__ == '__main__':
    main()
