from datetime import datetime
from functools import wraps
import sys
import time


def log_error(message):
    """Log an error message with a timestamp."""
    with open("error_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")


def delete_last_line():
    print ("\033[A                             \033[A")


def retry(retries=5, wait=2):
    """Decorator to retry a method call with specified retries and wait time."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal retries, wait
            attempts = retries
            while attempts > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log_error(f"Error during {func.__name__}: {str(e)}")
                    time.sleep(wait)
                    attempts -= 1
            return False

        return wrapper

    return decorator


"""
def extract_information(self, image_path: str, trys=30, wait=1):
    ""Tries to find an image and extract information from it.""
    cropped_image = image.crop((x1, y1, x2, y2))
    gray_cropped_image = cropped_image.convert("L")
    thresh_image = cv2.threshold(
        np.array(gray_cropped_image),
        0,
        255,
        cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV,
    )[1]
    result = pytesseract.image_to_string(thresh_image, config="--psm 7 digits")
    try:
        level = int(result.split()[0])
        return level
    except (IndexError, ValueError):
        log_error("Failed to read level from OCR result.")
        return 1
"""
