import eza_farming_bot
import sys
if __name__ == "__main__":
    print("###Program starting###\n")
    if "inf" in sys.argv:
        eza_farming_bot.inf()
    else: 
        eza_farming_bot.start()

    
    