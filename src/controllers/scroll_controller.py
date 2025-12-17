# controllers/scroll_controller.py
import time
from time import perf_counter

from utils.defines import STOPPED_MAX, STEP
from utils.context import ActionResult
from managers.file_manager import FileManager

fm = FileManager()

class ScrollController:

    @staticmethod
    def scroll_up(driver, scroll_area, step=STEP, max_scroll_time=STOPPED_MAX):
        start = perf_counter()

        if not scroll_area:
            return ActionResult(action="scroll_up",result="fail",elapsed_time=0,detail="scroll_area not found")

        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_area)
        client_height = driver.execute_script("return arguments[0].clientHeight;", scroll_area)

        if scroll_height <= client_height:
            return ActionResult(action="scroll_up",result="success",elapsed_time=perf_counter() - start,detail="no scrollable content")

        start_time = time.time()
        prev_top = driver.execute_script("return arguments[0].scrollTop;", scroll_area)

        while True:
            current_top = driver.execute_script(
                "return arguments[0].scrollTop;", scroll_area
            )

            if time.time() - start_time >= max_scroll_time:
                screenshot = fm.save_screenshot_png(driver, "scroll_up_timeout")
                return ActionResult(
                    action="scroll_up",
                    result="timeout",
                    elapsed_time=perf_counter() - start,
                    screenshot=screenshot
                )

            if current_top == 0 or current_top == prev_top:
                return ActionResult(
                    action="scroll_up",
                    result="success",
                    elapsed_time=perf_counter() - start,
                    detail="no more movement"
                )

            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1]);",
                scroll_area, -step
            )
            time.sleep(0.3)
            prev_top = current_top



    @staticmethod
    def scroll_down(driver, scroll_area, step=STEP, max_scroll_time=STOPPED_MAX):
        start = perf_counter()

        if not scroll_area:
            return ActionResult(action="scroll_down",result="fail",elapsed_time=0,detail="scroll_area not found")

        scroll_height = driver.execute_script("return arguments[0].scrollHeight;", scroll_area)
        client_height = driver.execute_script("return arguments[0].clientHeight;", scroll_area)

        if scroll_height <= client_height:
            return ActionResult(
                action="scroll_down",
                result="success",
                elapsed_time=perf_counter() - start,
                detail="no scrollable content"
            )

        start_time = time.time()
        prev_top = driver.execute_script(
            "return arguments[0].scrollTop;", scroll_area
        )

        while True:
            current_top = driver.execute_script(
                "return arguments[0].scrollTop;", scroll_area
            )

            if time.time() - start_time >= max_scroll_time:
                screenshot = fm.save_screenshot_png(driver, "scroll_down_timeout")
                return ActionResult(
                    action="scroll_down",
                    result="timeout",
                    elapsed_time=perf_counter() - start,
                    screenshot=screenshot
                )

            if current_top + client_height >= scroll_height or current_top == prev_top:
                return ActionResult(
                    action="scroll_down",
                    result="success",
                    elapsed_time=perf_counter() - start,
                    detail="no more movement"
                )

            driver.execute_script(
                "arguments[0].scrollBy(0, arguments[1]);",
                scroll_area, step
            )
            time.sleep(0.3)
            prev_top = current_top