import pyautogui as auto
from time import sleep

def scroll(scroll_distance: int):
    auto.mouseDown()
    # Simulate dragging the mouse down
    auto.move(0, scroll_distance, duration=1.0)  # Adjust the duration to control scroll speed

    # Release the mouse button
    auto.mouseUp()
def start():
    height = 1920
    width = 1080
    ok = auto.locateOnScreen("./Images/OK.jpeg",confidence=0.7)
    while not ok:    
        sleep(1)
        ok = auto.locateOnScreen("./Images/OK.jpeg",confidence=0.01)
        if ok:
            print("find")
            print(ok)
            auto.moveTo(ok,duration=1)
        else:
            print("cant find image")
        auto.click()

    while True:
        
        sleep(2)
        print(auto.position())
        auto.moveTo(963,665,duration=1)
        auto.click()
        sleep(5)
        print(auto.position())
        auto.moveTo(1146, 960,duration=1)
        auto.click()
        
        

def GetPosition():
    while True:
        print(auto.position())
        sleep(2)
    