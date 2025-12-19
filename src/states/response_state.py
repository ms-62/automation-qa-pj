import time
from enums.ui_status import AIresponse

from utils.defines import TIMEOUT_MAX, STOPPED_MAX

class ResponseState:
    def __init__(self, resp_btn_stop, stop_time=STOPPED_MAX, resp_timeout=TIMEOUT_MAX):
        self.resp_btn_stop = resp_btn_stop  # 함수형, lambda: WebElement
        self.stop_time = stop_time          # STOP 클릭 시점
        self.timeout = resp_timeout         # 최대 대기 시간

        self.start = time.monotonic()
        self.stop_clicked = False
        self.result = None

    def check(self):
        passed = time.monotonic() - self.start

        if passed >= self.timeout:
            self.result = AIresponse.TIMEOUT
            return True

        if passed >= self.stop_time and not self.stop_clicked:
            try:
                btn = self.resp_btn_stop()
                if btn and btn.is_enabled():
                    btn.click()
                    self.stop_clicked = True
                    self.result = AIresponse.STOPPED
                    return True
            except:
                pass

        return False