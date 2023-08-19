from time import sleep
from adbutils import adb
from adbutils._device import AdbDevice
import cv2
import numpy as np
import pytesseract
from PIL import Image
from typing import Callable
import datetime
def error(text)-> None:
    print(text)
    
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
    "./Images/FIGHT2.jpeg": "Click to start Fight",
    "./Images/START.jpeg": "Click to confirm battle",
    "./Images/End.jpeg": "Check if battle ends",
    "./Images/OK.jpeg": "Click OK button",
    "./Images/CANCEL.jpeg": "CLick in Cancel button",
    "./Images/SELECT.jpeg": "CLick to select Eza",
    "./Images/EXIT.jpeg": "Click to exit eza"
}   
    
class EZA():
    
    def __init__(self, device: AdbDevice, start: int = 0, end: int = 30) -> None:
        self.device = device
        self.start = start
        self.end = end

    def _find_and_click(self, image_path: str, trys=20,wait:int=1,special=0):
        """Return True if success else False """
        for _ in range(trys):
            find, x_pos, y_pos = self._find_image_position(image_path)
            if find:
                print(f"{PRINT_TEXT[image_path]}",end="\r")
                self.device.click(x_pos-special, y_pos)
                return True
            sleep(wait)
        return False
    
    def _find(self, image_path: str, trys=20,wait:int=1):
        """Return True if success else False """
        for _ in range(trys):
            find, _, _ = self._find_image_position(image_path)
            if find:
                return True
            sleep(wait)
        return False

    def _find_image_position(self, image_path: str):
        screenshot = np.array(self.device.screenshot().convert('RGB'))
        template_image = cv2.imread(image_path)
        return find_image_position(template_image,screenshot)

    def SelectLevel(self, trys=20, raise_error: bool=True):
        image_path = "./Images/SELECT.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def ExitLevel(self, trys=20, raise_error: bool=True):
        image_path = "./Images/EXIT.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def Fight(self, trys=20, raise_error: bool=True):
        image_path = "./Images/FIGHT2.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def Start(self, trys=20, raise_error: bool=True):
        image_path = "./Images/START.jpeg"
        if not self._find_and_click(image_path, trys):
            
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def OK(self, trys=20, raise_error: bool=True):
        image_path = "./Images/OK.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def End(self, trys=20, raise_error: bool=True):
        image_path = "./Images/End.jpeg"
        if not self._find_and_click(image_path, trys,wait=20,special=100):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    
    def Cancel(self, trys=20, raise_error: bool=True):
        image_path = "./Images/CANCEL.jpeg"
        if not self._find_and_click(image_path, trys,wait=20,special=100):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True

    def click_center_screen(self):
        x , y = self.device.window_size()
        print("Clicking at the center of the screen.",end="\r")
        self.device.click(x / 2,y / 2)
        
    def get_level(self,debug=False, zone: int = 1)-> int:
        screenshot = np.array(self.device.screenshot())
        pil_image = Image.fromarray(screenshot)

        # Crop the image to the specified region of interest
        if zone == 1: x1, y1, x2, y2 = 890, 570, 1010, 630
        else:
            x , y = self.device.window_size()
            center_x, center_y = x//2, y //2
            x1, y1, x2, y2 = center_x-100, center_y+335 , center_x+110, center_y + 458
        cropped_image = pil_image.crop((x1, y1, x2, y2))

        # Convert the cropped image to grayscale
        gray_cropped_image = cropped_image.convert('L')

        # Perform thresholding on the grayscale image
        thresh_image = cv2.threshold(src=np.array(gray_cropped_image), thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        
        # Display the cropped image for testing
        if debug: cropped_image.show()

        # Perform OCR on the thresholded image
        result: str = pytesseract.image_to_string(thresh_image, config="--psm 7 output digits")
        if result[0]:
            return int(result.split()[0])
        cropped_image.save(f"ERROR_{datetime.datetime.now()}.jpeg")
        quit("Unknow Eza level")
    
    def Swipe(self):
        x , y = self.device.window_size()
        self.device.swipe((x/2)+100,(y/2)+300,(x/2)-100,(y/2)+450,0.5)
    
    def WaitUntil(self, image_path: str, function: Callable[[], None], wait:int, trys=10, raise_error: bool=True):
        if not self._find(image_path, trys, wait):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        function()
        return True
        
import os

def start():
    
    device: AdbDevice = adb.device()
    eza = EZA(device)
    n = 0
    while True:
        print(f"Current levels complete: {n}")
        print("============================================")
        sleep(0.5)
        level: int = eza.get_level()
        if level < 31:
            n+=1
            print("Start eza",end="\r")
            
            eza.SelectLevel()
            for _ in range(31-level):
                
                sleep(0.5)
                eza.Fight()
                sleep(1)
                eza.Start()
                sleep(1)
                if not eza.End(20,raise_error=False):
                    print("lost batlle , change eza")
                    break
                sleep(1.5)
                eza.OK()
                sleep(1)
                if not eza.Cancel(trys=1,raise_error=False):
                    eza.OK()
                    eza.OK(trys=3,raise_error=False)
                sleep(1.5)
                eza.click_center_screen()
            eza.ExitLevel()
            os.system('cls' if os.name == 'nt' else 'clear')  
        print("Change EZA")
        
        eza.WaitUntil("./Images/SELECT.jpeg",function=eza.Swipe, wait=2) 
        
        
def inf():
    device: AdbDevice = adb.device()
    eza = EZA(device)
    while True:
        sleep(0.5)
        eza.Fight()
        sleep(1)
        eza.Start()
        sleep(1)
        if not eza.End(50,raise_error=False):
            print("lost batlle , change eza")
            break
        sleep(1.5)
        eza.OK()
        sleep(1)
        if not eza.Cancel(trys=1,raise_error=False):
            eza.OK()
            eza.OK(trys=3,raise_error=False)
        sleep(1)
        eza.click_center_screen()
 
             
        
  
            
        
        
        
        
        
   
        
        
        

    
""""""