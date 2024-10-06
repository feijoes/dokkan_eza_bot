from .custom_types import ImageLocation, DuelImageLocation
import cv2
import numpy as np
import pytesseract


class ImageProcessor:
    def extract_information(
        self, image, cords: tuple, ocr_config="--psm 7"
    ) -> str | None:
        """Processes a PIL image to extract text using Tesseract OCR.
            :param Image image: The PIL image to process.
            :param tuple cords: A tuple containing coordinates for cropping the image in the format (x1, y1, x2, y2).
            :param str ocr_config: (optional) Configuration string for Tesseract OCR. Defaults to "--psm 7".

        :return: The extracted text from the image. Returns a default message if extraction fails.
        :rtype: str
        """
        cropped_image = image.crop(cords)
        gray_cropped_image = cropped_image.convert("L")

        # Apply thresholding for better OCR results
        thresh_image = cv2.threshold(
            np.array(gray_cropped_image),
            0,
            255,
            cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV,
        )[1]
        # Perform OCR to extract text
        try:
            result = pytesseract.image_to_string(
                thresh_image, config=ocr_config
            ).strip()
        except Exception as e:
            print(e)
            return None
        return result

    def find_dual_images(
        self, image1: str, image2: str, screenshot, threshold=0.8
    ) -> DuelImageLocation:
        """Tries to find two images at the same time
            :param image_path_1: Path to the first image to search for.
            :param image_path_2: Path to the second image to search for.
        :return:
        - (0, x1, y1) if the first image is found,
        - (1, x2, y2) if the second image is found,
        - (-1, None, None) if neither image is found after all attempts.
        """
        
        find_1, x1, y1 = self.find_image_position(image1, screenshot, threshold)
        find_2, x2, y2 = self.find_image_position(image2, screenshot, threshold)
        if find_1:
            return 0, x1, y1
        elif find_2:
            return 1, x2, y2
        return -1, None, None

    def is_image_present(
        self, image_path: str, search_image_path: str, threshold=0.4
    ) -> bool:
        """Find an image within another image using cv2."""
        result = cv2.matchTemplate(image_path, search_image_path, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val >= threshold:
            return True
        else:
            return False

    def find_image_position(
        self, image: str, screenshot, threshold=0.8
    ) -> ImageLocation:
        """Find the position of an image in a scene."""
        # Convert both images to grayscale
        target_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        # Get the maximum correlation value and its location
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            h, w = template_gray.shape
            x, y = max_loc
            center_x = x + w // 2
            center_y = y + h // 2
            return True, center_x, center_y
        else:
            return False, None, None
