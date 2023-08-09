# Dokkan Battle EZA Farming Bot

![Dokkan Battle Auto-Play Script](https://github.com/feijoes/dokkan_eza_bot/assets/74252371/c2f5c2bf-1e0c-4ebe-8792-ec55113311ce)

## Introduction

The Dokkan Battle EZA Farming Bot is a Python script designed to automate the process of farming the Extreme Z-Awakening levels in Dragon Ball Z Dokkan Battle. The script runs on your computer and interacts with the game on your phone.

_This bot is no a autoclicker_; it not only completes the levels but also manages the current level of the EZA and switches between different EZAs.

***This bot is still in beta version***

The bot's functionality is not yet complete, and there are issues such as being able to complete 30 levels of LR EZAs.

## Features

- Automated farming of Extreme Z-Awakening levels in Dokkan Battle.
- It identifies buttons and actions using images, so it can adapt to different screen sizes and resolutions.
- Can swipe bettwen eza and only 

## Requirements

1. You need an Android device with USB debugging enabled. This allows the script to communicate with the phone via a USB cable.
2. Get you phone in [developers options](https://www.digitaltrends.com/mobile/how-to-get-developer-options-on-android/) and enable the options:
      * **Dont lock screen**: This prevents the screen from locking to ensure uninterrupted gameplay.
      * **USB Debbuging**

4. Your computer should have Python 3.x installed. You can download it from the [official Python website](https://www.python.org/downloads/).
5. Install [tesseract](https://linuxhint.com/install-tesseract-windows/) in your computer

## Usage

1. Launch the Dokkan Battle app on your Android device and go to eza section
2. Scroll down to the bottom of the EZA events, as the bot will change EZA events by swiping upwards.
3. Open a terminal or command prompt in the project directory.
4. install the requirements
  ```py
  pip install -r requirements.txt
  ```
  And run 
  ```
  python main.py
  ```

## Disclaimer

This project is intended for educational and personal use only. The use of automation bots in games may violate the game's terms of service, and using this script may carry the risk of account suspension or banning. The developer of this project is not responsible for any consequences resulting from the use of this bot.

## Contributing

Contributions to this project are welcome! If you encounter any issues, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to modify the README according to your project's specific details, and don't forget to add a proper license file (e.g., `LICENSE`) to your project if you plan to share it with others.
