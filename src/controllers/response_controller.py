import time
from states.response_state import ResponseState
from enums.ui_status import AIresponse

from utils.defines import TIMEOUT_MAX, STOPPED_MAX

class ResponseController:

    @staticmethod
    def until(condition, timeout = TIMEOUT_MAX):
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            try:
                if condition():
                    return True
            except:
                pass
            time.sleep(0.3)
        return False
    
    # stop_time에 취소
    @staticmethod
    def wait_for_response_with_timeout(btn_stop, stop_time = STOPPED_MAX, timeout = TIMEOUT_MAX):
        state = ResponseState(
            resp_btn_stop=btn_stop,
            stop_time=stop_time,
            resp_timeout=timeout
        )

        finished = ResponseController.until(
            condition=state.check,
            timeout=timeout 
        )

        return state.result if finished else AIresponse.TIMEOUT

    # 20초가 지났는데 답변을 못찾는다 time_out 
    # 찾으면 complete
    @staticmethod
    def wait_for_complete(ai_response_area_getter, timeout=TIMEOUT_MAX):
        """
        AI 응답 영역이 완료될 때까지 대기
        ai_response_area_getter: AI 응답 영역을 반환하는 함수
        """
        result_state = {"result": AIresponse.NONE}

        def condition():
            try:
                area = ai_response_area_getter()
                if area and area.get_attribute("data-status") == "complete":
                    result_state["result"] = AIresponse.COMPLETED
                    return True
            except:
                pass
            return False

        finished = ResponseController.until(condition=condition, timeout=timeout)
        return result_state["result"] if finished else AIresponse.TIMEOUT