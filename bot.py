import pyautogui as auto
from time import sleep
from pathlib import Path

# pyautogui Functions

def MoveAndClick(x:int, y:int, clicks:int=1 ,duration:int = 1):
    auto.moveTo(x,y,duration=duration)
    for _ in range(clicks):
        sleep(1)
        auto.click()
    
def scroll(scroll_distance: int,duration:int = 1):
    """
    Perform a custom scroll since pyautogui.scroll() does not work on mobile devices.

    Parameters:
        scroll_distance (int): The distance to scroll in pixels. Positive value scrolls down, negative scrolls up.

    Note:
        This function simulates a mouse drag to achieve scrolling. Adjust the 'duration' parameter in auto.move()
        to control the scroll speed.

    Example:
        custom_scroll(100)  # Scrolls the screen down by 100 pixels.
        custom_scroll(-50)  # Scrolls the screen up by 50 pixels.
    """
    auto.mouseDown()
    auto.move(0, scroll_distance, duration=duration)
    auto.mouseUp()
# Dont work in low Quality    
def locateAndClick(imagePath: Path ,confidence: int, attempts:int) -> None:
    
    image = None
    n = 0
    while not image:
        sleep(1)
        image = auto.locateOnScreen(imagePath,confidence=confidence)
        if image:
            auto.moveTo(image,duration=1)
            auto.click()
            break
        n+=1
        if n == attempts:
            raise BaseException("Not found " + imagePath)
        
class EZA():
    def __init__(self, start:int = 0, end:int = 30) -> None:
        self.start = start
        self.end = end
        
    def StartLevel(self):
        MoveAndClick(963,665)
    
    def StartFight(self):
        MoveAndClick(1146,960)
    
    def EndFight(self):
        """Click in """
        MoveAndClick(947, 944,clicks=2)
    def EndFriend(self):
        MoveAndClick(890, 678,clicks=2)
        

        

def start():
    height = 1920
    width = 1080
    test= EZA(2)
    for i in range(test.start,test.end):
        sleep(2)
        test.StartLevel()
        sleep(20)
        test.StartFight()
        sleep(i * 10 + 45)
        test.EndFight()
        sleep(1)
        test.EndFriend()
        
        
        
        

    
        
# Developer Functions        
def GetPosition():
    while True:
        print(auto.position())
        sleep(2)