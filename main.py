import subprocess
import bot
from time import sleep
import sys
def run_scrcpy() :
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
    return subprocess.Popen(command)
    

if __name__ == "__main__":
    process = run_scrcpy()
    try:
        
        if "pos" in sys.argv:
            print("Printing positions")
            bot.GetPosition()
        else:
            sleep(4)
            print("Program starting")
            bot.start()
    except BaseException as e:
        process.terminate()
        print(e)     
    
    