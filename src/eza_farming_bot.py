from adbutils import adb
from adbutils._device import AdbDevice
from .bot import Bot
from PIL import Image
from .utils import log_error, retry
import cv2
import numpy as np
import os
import time


class EZA(Bot):
    @retry(retries=3)
    def SelectLevel(self, isLREZA: bool, raise_error: bool = True):
        """Select level with retry logic."""
        image_path = "./Images/EZA.jpeg" if not isLREZA else "./Images/LREZA.jpeg"
        self._perform_action(image_path, raise_error=raise_error)

    @retry(retries=3)
    def ExitLevel(self, raise_error: bool = True):
        """Exit level with retries on fail."""
        self._perform_action("./Images/EXIT.jpeg", raise_error=raise_error)

    @retry(retries=3)
    def Fight(self, raise_error: bool = True):
        """Initiate a fight, retrying on initial failures."""
        self._perform_action("./Images/STA.jpg", raise_error=raise_error)

    @retry(retries=3)
    def Start(self, raise_error: bool = True):
        """Start a level, with retries on failures."""
        self._perform_action("./Images/START.jpg", raise_error=raise_error)

    @retry(retries=3)
    def OK(self, raise_error: bool = True):
        """Click OK with retries."""
        self._perform_action("./Images/OK.jpeg", raise_error=raise_error)

    def Cancel(self, raise_error: bool = True):
        """Attempt to cancel with retry logic."""
        return self._perform_actionFaster("./Images/CANCEL.jpeg", raise_error=False)

    @retry(retries=3)
    def End(self, raize_error: bool = True):
        """Handle end of battle with retry logic."""
        battle_status = self._find_dual_images(
            "./Images/END.jpg", "./Images/STA.jpg", wait=10
        )
        if battle_status[0] == -1 and raize_error:
            self._handle_error("'END' nor 'STA'")
        elif battle_status[0] == 0:
            self.device.click(battle_status[1] - 150, battle_status[2])
        elif battle_status[0] == 1:
            return False
        return True

    @retry(retries=3)
    def get_level(self, zone: int = 1) -> int:
        """Get the current level using OCR with retries on fail."""
        pil_image = Image.fromarray(np.array(self.device.screenshot()))

        x1, y1, x2, y2 = 890, 570, 1010, 630
        if zone != 1:
            _, x, y = self.get_image_position("./Images/NEXT.jpeg")

            if x and y:
                x1, y1, x2, y2 = x - 40, y + 40, x + 80, y + 100

        level = self.img_processor.extract_information(
            pil_image, (x1, y1, x2, y2), ocr_config="--psm 7 digits"
        )
        try:
            return int(level.split()[0])
        except (IndexError, ValueError):
            log_error("Failed to read level from OCR result.")
            return 1  #

    def isLR(self) -> bool:
        """Check if eza stage is LR or not."""
        screenshot = np.array(self.device.screenshot().convert("RGB"))
        template_image = cv2.imread("./Images/LREZA.jpeg")
        return self.img_processor.find_image_in_another(
            template_image, screenshot, 0.63
        )


def start(debug: bool):
    device: AdbDevice = adb.device()
    eza = EZA(device, debug=debug)
    n = 0
    while True:
        time.sleep(0.5)
        level: int = eza.get_level(2)
        maxlevel = 11 if eza.isLR() else 31
        if level < maxlevel:
            print("Start eza", end="\r")
            eza.SelectLevel(isLREZA=maxlevel == 11)
            for _ in range(maxlevel - level):
                print(f"Current levels complete: {n}")
                print("============================================")
                time.sleep(0.5)
                eza.Fight()
                time.sleep(1)
                eza.Start()
                time.sleep(1)
                if not eza.End():
                    print("Battle lost, change eza")
                    break
                time.sleep(1.5)
                eza.OK()
                time.sleep(1)
                if not eza.Cancel(raise_error=False):
                    eza.handle_friend_request()
                time.sleep(1.5)
                eza._click_center_screen()
                n += 1
                os.system("cls" if os.name == "nt" else "clear")
            eza.ExitLevel()

        print("Change EZA")
        if not eza._wait_util("./Images/EZA.jpeg", wait=5):
            print("Could not change EZA")
            eza._handle_error("./Images/EZA.jpeg")
            break
        eza._swipe()


def inf(no_lost: bool):
    device: AdbDevice = adb.device()
    eza = EZA(device)
    n = 0
    while True:
        print(
            f"Current levels complete: {n}\n============================================"
        )
        n += 1
        time.sleep(0.5)
        eza.Fight()
        time.sleep(1)
        eza.Start()
        time.sleep(1)
        print("Waiting for battle to end")
        if not eza.End():
            print("Battle lost")
            if not no_lost:
                break
            continue
        time.sleep(1.5)
        eza.OK()
        time.sleep(1)
        if not eza.Cancel(raise_error=False):
            eza.OK()
        time.sleep(1)
        eza._click_center_screen()
        os.system("cls" if os.name == "nt" else "clear")
