from adbutils import adb
from src.image import ImageProcessor
import cv2
import numpy as np

device = adb.device()

image_path = "Images/OK2.jpeg"
image_processor = ImageProcessor()


class Debug:
    @staticmethod
    def draw_rectangle_around_match(screenshot, top_left, w, h):
        cv2.rectangle(
            screenshot, top_left, (top_left[0] + w, top_left[1] + h), (255, 0, 0), 2
        )
        cv2.imshow("Matched Image", screenshot)
        cv2.setWindowProperty("Matched Image", 1, cv2.WINDOW_NORMAL)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


screenshot = np.array(device.screenshot().convert("RGB"), dtype=np.uint8)
template_image = cv2.imread(image_path)

found, x, y = image_processor.find_image_position(
    template_image, screenshot, threshold=0.8
)

if found:
    Debug.draw_rectangle_around_match(screenshot, (x, y), *template_image.shape[:2])
else:
    print(f"Image {image_path} not found in current screen.")
