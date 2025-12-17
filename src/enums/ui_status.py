from enum import Enum, auto


# 요즘엔 숫자를 쓰지않고 auto()를 쓴다고 한다.
class AIresponse(Enum):
    NONE = auto()
    COMPLETED = auto()   # ai가 응답을 완료한 상태
    STOPPED = auto()     # 취소 버튼을 클릭한 상태
    TIMEOUT = auto()     # 무한 로딩 상태(15초 이상으로 기준)
    
class MenuStatus(Enum):
    NONE = auto()
    OPENED = auto()
    CLOSED = auto()
    
class ModelState(Enum):
    ENABLED = auto()    # 활성화 모델
    DISABLED = auto()   # 비활성화
    ALWAYS_ON = auto()  # 항상 켜두는 것
    