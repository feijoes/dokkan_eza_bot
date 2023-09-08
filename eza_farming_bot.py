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
    
def find_image_in_another(source_image, template, threshold:int=0.8) -> bool:
    result = cv2.matchTemplate(source_image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return True
    else:
        return False


# Path to the source image and the template image
PRINT_TEXT = { 
    "./Images/FIGHT.jpeg": "Click to start Fight",
    "./Images/FIGHT2.jpeg": "Click to start Fight",
    "./Images/START.jpeg": "Click to confirm battle",
    "./Images/End.jpeg": "Battle ends",
    "./Images/OK.jpeg": "Click OK button",
    "./Images/CANCEL.jpeg": "CLick in Cancel button",
    "./Images/EZA.jpeg": "CLick to select EZA",
    "./Images/EXIT.jpeg": "Click to exit EZA",
    "./Images/LREZA.jpeg":"CLick to select LR EZA",
}   

import sys

def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    
class EZA():
    
    def __init__(self, device: AdbDevice, debug: bool=False) -> None:
        self.device = device
        self.debug = debug

    def _find_and_click(self, image_path: str, trys=30,wait:int=1,special=0):
        """Return True if success else False """
        for _ in range(trys):
            find, x_pos, y_pos = self._find_image_position(image_path)
            if find:
                print(f"{PRINT_TEXT[image_path]}",end="\r")
                self.device.click(x_pos-special, y_pos)
                return True
            
            for i in range(1,wait+1):
                print("Waiting loading"+ "." * (i % 4))
                delete_last_line()
                sleep(1)
        return False
    
    def _find(self, image_path: str, trys=30,wait:int=1):
        """Return True if success else False """
        for _ in range(trys):
            find, _, _ = self._find_image_position(image_path)
            if find:
                return True
            sleep(wait)
        return False

    def _find_dual_images(self, image_path_1: str, image_path_2: str, trys=30, wait=1):
        """
        Tries to find two images at the same time.
        
        :param image_path_1: Path to the first image to search for.
        :param image_path_2: Path to the second image to search for.
        :param trys: Number of attempts to find the images.
        :param wait: Time to wait between attempts.
        :return: If the first image is found, returns (0, x1, y1).
                If the second image is found, returns (1, x2, y2).
                If neither image is found, returns None.
        """
        for _ in range(trys):
            find_1, x1, y1 = self._find_image_position(image_path_1)
            find_2, x2, y2 = self._find_image_position(image_path_2)
            
            if find_1:
                return 0, x1, y1
            elif find_2:
                return 1, x2, y2
            
            for i in range(1, wait + 1):
                if image_path_1 == "./Images/End.jpeg":
                    print("Waiting for the battle to end" + "." * (i % 4))
                else:
                    print("Waiting loading" + "." * (i % 4))
                delete_last_line()
                sleep(1)
        return None
    def _find_image_position(self, image_path: str):
        screenshot = np.array(self.device.screenshot().convert('RGB'))
        template_image = cv2.imread(image_path)
        return find_image_position(template_image,screenshot)

    def SelectLevel(self, isLREZA: bool ,trys=30, raise_error: bool=True):
        image_path = "./Images/EZA.jpeg" if not isLREZA else "./Images/LREZA.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def ExitLevel(self, trys=30, raise_error: bool=True):
        image_path = "./Images/EXIT.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def Fight(self, trys=30, raise_error: bool=True):
        image_path = "./Images/FIGHT2.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def Start(self, trys=30, raise_error: bool=True):
        image_path = "./Images/START.jpeg"
        if not self._find_and_click(image_path, trys):
            
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def OK(self, trys=30, raise_error: bool=True):
        image_path = "./Images/OK.jpeg"
        if not self._find_and_click(image_path, trys):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True
    def End(self, trys=45):
        image_path_1 = "./Images/End.jpeg"
        image_path_2 =  "./Images/FIGHT2.jpeg"
        battle_end = self._find_dual_images(image_path_1, image_path_2, trys, wait=13)
        if battle_end == None:
            self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
            error(f"Template {image_path_1} or {image_path_2} is not present in the target image.")
        elif battle_end[0] == 0:
            self.device.click(battle_end[1]-100, battle_end[2])
        elif battle_end[0] == 1:
            return False
        return True
    
    def Cancel(self, trys=30, raise_error: bool=True):
        image_path = "./Images/CANCEL.jpeg"
        if not self._find_and_click(image_path, trys,wait=5,special=self.device.window_size()[0] // 4):
            if raise_error:
                self.device.screenshot().save(f"ERROR_{datetime.datetime.now()}.jpeg")
                error(f"Template {image_path} is not present in the target image.")
            return False
        return True

    def click_center_screen(self):
        x , y = self.device.window_size()
        print("Clicking at the center of the screen.",end="\r")
        self.device.click(x / 2,y / 2)
        
    def get_level(self, zone: int = 1)-> int:
        screenshot = np.array(self.device.screenshot())
        pil_image = Image.fromarray(screenshot)
        
        # Crop the image to the specified region of interest
        if zone == 1: x1, y1, x2, y2 = 890, 570, 1010, 630
        else:
            _, x , y = self._find_image_position("./Images/NEXT.jpeg")
            if not x:
                x1, y1, x2, y2 = 890, 570, 1010, 630
            else:
                x1, y1, x2, y2 = x-40, y+40 , x+80, y + 100
        cropped_image = pil_image.crop((x1, y1, x2, y2))
        
        # Convert the cropped image to grayscale
        gray_cropped_image = cropped_image.convert('L')

        # Perform thresholding on the grayscale image
        thresh_image = cv2.threshold(src=np.array(gray_cropped_image), thresh=0, maxval=255, type=cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]
        
        # Display the cropped image for testing
        

        # Perform OCR on the thresholded image
        result: str = pytesseract.image_to_string(thresh_image, config="--psm 7 output digits")
        if self.debug: 
            print(result)
            cropped_image.show()
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
    
    def isLR(self)-> bool:
        screenshot = np.array(self.device.screenshot().convert('RGB'))
        template_image = cv2.imread("./Images/LREZA.jpeg")
        return find_image_in_another(template_image, screenshot, 0.63)
        
        
import os

def start(debug:bool):
    
    device: AdbDevice = adb.device()
    eza = EZA(device,debug=debug)
    n = 0
    while True:
        sleep(0.5)
        # if error in  get_level() change number to 1
        
        level: int = eza.get_level(2)
        maxlevel = 11 if eza.isLR() else 31
        if level < maxlevel:
        
            print("Start eza",end="\r")
            eza.SelectLevel(isLREZA=maxlevel==11)
            for _ in range(maxlevel-level):
                print(f"Current levels complete: {n}")
                print("============================================")
                sleep(0.5)
                eza.Fight()
                sleep(1)
                eza.Start()
                sleep(1)
                
                if not eza.End(35):
                    print("Batlle lost , change eza")
                    break 
                sleep(1.5)
                eza.OK()
                sleep(1)
                if not eza.Cancel(trys=1,raise_error=False):
                    eza.OK()
                    eza.OK(trys=2,raise_error=False)
                sleep(1.5)
                eza.click_center_screen()
                n+=1
                os.system('cls' if os.name == 'nt' else 'clear')  
            eza.ExitLevel()
            
        print("Change EZA")
        
        eza.WaitUntil("./Images/EZA.jpeg",trys=30,function=eza.Swipe, wait=5) 
        
        

def inf():
    device: AdbDevice = adb.device()
    eza = EZA(device)
    n=0
    while True:
        print(f"Current levels complete: {n}\n============================================")
        n+=1
        sleep(0.5)
        eza.Fight()
        sleep(1)
        eza.Start()
        sleep(1)
        if not eza.End(50):
            print("Batlle lost")
            break
        sleep(1.5)
        eza.OK()
        sleep(1)
        if not eza.Cancel(trys=1,raise_error=False):
            eza.OK()
            eza.OK(trys=2,raise_error=False)
        sleep(1)
        eza.click_center_screen()
        os.system('cls' if os.name == 'nt' else 'clear')  

            
        
        
        
        
        
   
        
        
        

    
""""""