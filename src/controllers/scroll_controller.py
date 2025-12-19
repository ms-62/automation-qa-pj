import time
from utils.defines import STEP

class ScrollController:

    @staticmethod
    def scroll_up(driver, scroll_area, step=STEP, delay = 0.5):
        if not scroll_area:
            return

        while True:
            current_top = driver.execute_script("return arguments[0].scrollTop;", scroll_area)
            if current_top <= 0:
                break  
            
            driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scroll_area, -step)
            time.sleep(delay)

    @staticmethod
    def scroll_down(driver, scroll_area, step=STEP, delay=0.5):
        if not scroll_area:
            return

        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_area)
        client_height = driver.execute_script("return arguments[0].clientHeight;", scroll_area)

        while True:
            current_top = driver.execute_script("return arguments[0].scrollTop;", scroll_area)
            if current_top + client_height >= scroll_height:
                break  
            
            driver.execute_script("arguments[0].scrollBy(0, arguments[1]);", scroll_area, step)
            time.sleep(delay)
