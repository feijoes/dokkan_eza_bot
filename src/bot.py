from adbutils._device import AdbDevice
from datetime import datetime
from .image import ImageProcessor
from waiting import wait as wait_for, TimeoutExpired
import cv2
import json
import numpy as np
import time
from .utils import (
    log_error,
    delete_last_line,
)

with open("messages.json", "r") as f:
    PRINT_TEXT = json.load(f)


class Bot:
    def __init__(self, device: AdbDevice, debug: bool = False) -> None:
        self.device = device
        self.debug = debug
        self.img_processor = ImageProcessor()

    def get_image_position(self, image_path: str):
        screenshot = np.array(self.device.screenshot().convert("RGB"))
        template_image = cv2.imread(image_path)
        return self.img_processor.find_image_position(template_image, screenshot)

    def _find_and_click(self, image_path: str, trys=30, wait=1, special=0):
        """Attempts to find and click on an image, retrying on failure."""
        for _ in range(trys):
            find, x_pos, y_pos = self.get_image_position(image_path)
            if find:
                print(f"{PRINT_TEXT[image_path]}", end="\r")
                self.device.click(x_pos - special, y_pos)
                return True
            for i in range(1, wait + 1):
                print("Waiting loading" + "." * (i % 4))
                delete_last_line()
                time.sleep(1)
        return False

    def _find(self, image_path: str, trys=30, wait: int = 1):
        """Return True if success else False"""
        for _ in range(trys):
            find, _, _ = self.get_image_position(image_path)
            if find:
                return True
            time.sleep(wait)
        return False

    def _find_dual_images(
        self, image_path1: str, image_path2: str, trys: int = 30, wait: int = 1
    ):
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)
        for _ in range(trys):
            screenshot = np.array(
                self.device.screenshot().convert("RGB"), dtype=np.uint8
            )
            result = self.img_processor.find_dual_images(image1, image2, screenshot)
            if result[0] != -1:
                return result
            time.sleep(wait)
        return False

    def _swipe(self):
        x, y = self.device.window_size()
        self.device.swipe(
            (x / 2) + 100, (y / 2) + 300, (x / 2) - 100, (y / 2) + 450, 0.5
        )

    def _click_center_screen(self):
        x, y = self.device.window_size()
        print("Clicking at the center of the screen.", end="\r")
        self.device.click(x / 2, y / 2)

    def _wait_util(
        self,
        image_path: str,
        wait: int,
        trys=10,
        raise_error: bool = True,
    ):
        """Wait for an image to be present and return True if found else False."""
        try:
            wait_for(lambda: self._find(image_path, trys, wait), timeout_seconds=10)
        except TimeoutExpired:
            if raise_error:
                self._handle_error(image_path)
            return False
        return True

    def _handle_error(self, image_path: str) -> None:
        """Handle errors by taking a screenshot and logging the issue."""
        self.device.screenshot().save(
            f"error/ERROR_{datetime.now().strftime('%H_%M_%S')}.jpeg"
        )
        log_error(f"Template {image_path} is not present in the target image.")

    def _perform_action(
        self, image_path: str, trys=30, raise_error: bool = True
    ) -> bool:
        """Perform an action by finding and clicking the image, with retries and error handling."""
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self._handle_error(image_path)
            return False
        return True
