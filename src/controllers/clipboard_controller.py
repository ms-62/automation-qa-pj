import pyperclip
import platform
import pyautogui
import time

from selenium.webdriver.common.keys import Keys

class ClipboardController:

    @staticmethod
    def copy(text: str):
        pyperclip.copy(text)

    @staticmethod
    def paste(element):
        system = platform.system()
        if system == "Darwin":  # 맥용!
            element.send_keys(Keys.COMMAND, "V")
        else:                   # 윈도우 용!
            element.send_keys(Keys.CONTROL, "V")

    @staticmethod
    def read():
        try:
            return pyperclip.paste().strip()
        except Exception:
            return ""
    
    @staticmethod
    def paste_file_path(file_path):
        system = platform.system()   
        if system == "Darwin": # 맥용!

            pyautogui.keyDown("command")
            pyautogui.keyDown("shift")
            pyautogui.press("g")
            pyautogui.keyUp("shift")
            pyautogui.keyUp("command")
            time.sleep(1)
            pyautogui.hotkey("command", "v")
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.press("enter") 
            time.sleep(1)
        else: # 윈도우 용!
            pyautogui.write(file_path, interval=0.03)
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(1)
            pass
        
    