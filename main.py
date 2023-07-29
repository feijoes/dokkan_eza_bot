import subprocess
import bot
from time import sleep
import sys
def run_scrcpy():
    command = [
        "scrcpy",
        "--turn-screen-off",
        "--disable-screensaver",
        "--show-touches",
        "--stay-awake",
        "--max-fps=144",
        "-m400", 
        "-f"
        
    ]

    try:
        subprocess.Popen(command)
    except subprocess.CalledProcessError as e:
        print(f"Error while running scrcpy: {e}")
    except FileNotFoundError:
        print("scrcpy not found. Make sure it is installed and available in your PATH.")

if __name__ == "__main__":
    run_scrcpy()
    if "pos" in sys.argv:
        print("Printing positions")
        bot.GetPosition()
    else:
        sleep(2)

        print("Program starting")
        bot.start()
    
    