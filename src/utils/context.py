from dataclasses import dataclass

from utils.defines import TARGET_URL

@dataclass
class LoginContext:
    driver: object
    fm: object
    login_page: object
    main_page: object
    member_page: object
    agent_page : object
    user_data: list
    file_name: str = "cookies.json"
    url: str = TARGET_URL["MAIN_URL"]
    
    
@dataclass
class TextContext:
    test_name: str
    page: str

@dataclass
class ActionResult:
    action: str
    result: str                     # "success" ? "fail" ?
    elapsed_time: float
    detail: str = ""                # 실패 이유 등 성공 된곳? 
    screenshot: str | None = None   # 스크린샷 경로   
