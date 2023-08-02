from time import sleep
from adbutils import adb
from adbutils._device import AdbDevice
import cv2
import numpy as np
import pytesseract
from PIL import Image

def error(image_name)-> None:
    print(f"Template {image_name} is not present in the target image.")
    quit()
    
def find_image_position(template_image: str,screenshot, threshold=0.8):
    # Load the target image and the template image

    # Convert both images to grayscale
    target_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
   
    # Get the maximum correlation value and its location
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    # Check if the maximum correlation value is greater than the threshold
 
    if max_val >= threshold:
        h, w = template_gray.shape
        x, y = max_loc
        center_x = x + w // 2
        center_y = y + h // 2
        return True, center_x, center_y
    else:
        return False, None, None

PRINT_TEXT = { 
    "./Images/FIGHT.jpeg": "Click to start Fight",
    "./Images/START.jpeg": "Click to confirm battle",
    "./Images/End.jpeg": "Check if battle ends",
    "./Images/OK.jpeg": "Click OK button",
}   
    
class EZA():
    
    def __init__(self, device: AdbDevice, start: int = 0, end: int = 30) -> None:
        self.device = device
        self.start = start
        self.end = end

    def _find_and_click(self, image_path: str, trys=10,wait:int=1):
        for _ in range(trys):
            find, x_pos, y_pos = self._find_image_position(image_path)
            if find:
                print(f"{PRINT_TEXT[image_path]}")
                self.device.click(x_pos, y_pos)
                return True
            sleep(wait)
        return False

    def _find_image_position(self, image_path: str):
        screenshot = np.array(self.device.screenshot().convert('RGB'))
        template_image = cv2.imread(image_path)
        return find_image_position(template_image,screenshot)

    def Fight(self, trys=10):
        image_path = "./Images/FIGHT.jpeg"
        if not self._find_and_click(image_path, trys):
            error(image_path)
            return False
        return True
    def Start(self, trys=10):
        image_path = "./Images/START.jpeg"
        if not self._find_and_click(image_path, trys):
            error(image_path)
            return False
        return True
    def OK(self, trys=10):
        image_path = "./Images/OK.jpeg"
        if not self._find_and_click(image_path, trys):
            error(image_path)
            return False
        return True
    def End(self, trys=10):
        image_path = "./Images/End.jpeg"
        if not self._find_and_click(image_path, trys,wait=20):
            error(image_path)
            return False
        return True
    def click_center_screen(self):
        x , y = self.device.window_size()
        print("Clicking at the center of the screen.")
        self.device.click(x / 2,y / 2)
        
    def get_level(self)-> int:
        screenshot = np.array(self.device.screenshot())
        pil_image = Image.fromarray(screenshot)

        # Crop the image to the specified region of interest
        x1, y1, x2, y2 = 890, 570, 1010, 630
        cropped_image = pil_image.crop((x1, y1, x2, y2))

        # Convert the cropped image to grayscale
        gray_cropped_image = cropped_image.convert('L')

        # Perform thresholding on the grayscale image
        thresh_image = cv2.threshold(src=np.array(gray_cropped_image), thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

        # Display the cropped image for testing
        cropped_image.show()

        # Perform OCR on the thresholded image
        result: str = pytesseract.image_to_string(thresh_image, config="--psm 7 output digits")
        
        return int(result.split()[0])

    
       
def start():
    
    device: AdbDevice = adb.device()
    eza = EZA(device)
    while True:
        sleep(1)
        eza.Fight()
        sleep(1)
        eza.Start()
        sleep(1)
        eza.End(20)
        sleep(0.5)
        eza.OK()
        sleep(0.5)
        eza.OK()
        sleep(0.5)
        eza.click_center_screen()
  
            
        
        
        
        
        
   
        
        
        

    
