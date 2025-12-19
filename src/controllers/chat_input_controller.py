import time
import platform
from selenium.webdriver.common.keys import Keys
from controllers.clipboard_controller import ClipboardController
from selenium.webdriver.support.ui import WebDriverWait

class ChatInputController:

    @staticmethod
    def send_text(element, text: str):
        element.click()
        element.send_keys(text)

    @staticmethod
    def paste_text(element, text: str):
        ClipboardController.copy(text)
        element.click()
        ClipboardController.paste(element)
        
    @staticmethod
    def reset_text(element):
        element.click()
        time.sleep(1)
        
        system = platform.system()
        if system == "Darwin": # 맥용!
            element.send_keys(Keys.COMMAND, "A")
        else:   # 윈도우 용!
            element.send_keys(Keys.CONTROL, "A")
        time.sleep(1)
        element.send_keys(Keys.BACK_SPACE)
        time.sleep(1)
        
