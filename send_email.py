import os
import smtplib
from email.message import EmailMessage
# import imghdr  # imghdr became deprecated
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()


SENDER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(image_path):
    """
    Sends an email with an image attachment.

    Args:
        image_path (pathlib.Path): The path to the image file to be attached.

    Returns:
        bool: True if the email was successfully sent, False otherwise.
    """

    email_message = EmailMessage()  # Create an EmailMessage object
    email_message["Subject"] = "New person showed up!"  # Set email subject
    email_message.set_content(
        "Hey, we just saw a new person approaching!")  # Set email content

    # Get the content and the type of the image file
    img_content, img_type = read_image_content(image_path)

    # Add the image file as an attachment to the email message
    email_message.add_attachment(
        img_content, maintype='image', subtype=img_type)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp_server:

            smtp_server.ehlo()  # Introduce ourselves to the server
            smtp_server.starttls()  # Upgrade the connection to a secure one using TLS
            smtp_server.login(SENDER, PASSWORD)  # Login to the SMTP server
            # Send the email via SMTP after converting the message to a string
            smtp_server.sendmail(SENDER, RECEIVER, email_message.as_string())

        return True  # Return True if the email was successfully sent

    except smtplib.SMTPException as e:
        # Display error if an SMTPException occurs
        print(f"\nError: Failed to send email - {e}\n")

        return False  # Return False indicating failure to send email


def read_image_content(image_path):
    """
    Reads the content of an image file and determines its type.

    Args:
        image_path (pathlib.Path): The path to the image file.

    Returns:
        tuple or None: A tuple containing the content of the image file as bytes and its type,
        or None if an error occurs.
    """
    try:
        with open(image_path, 'rb') as bin_file:
            image_content = bin_file.read()
            # image_type = imghdr.what(None, image_content)

        # Since 'imghdr' is deprecated, Use Pillow instead and open the image file to inspect its format
        with Image.open(image_path) as img:
            # Get the format of the image (e.g., 'JPEG', 'PNG', 'GIF', etc.) then convert it to lowercase
            image_type = img.format.lower()

        return image_content, image_type

    except Exception as e:
        print(f"\nError: {e}\n")

        return None, None  # Return None for both content and type if an error occurs


if __name__ == "__main__":

    test_img_path = Path("./Notes") / "detecting_object_on_cam_logic.png"

    if send_email(test_img_path):
        print("\nEmail sent successfully.\n")
    else:
        print("\nFailed to send email. Please try again later.\n")
