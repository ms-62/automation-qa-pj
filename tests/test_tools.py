import os
from utils.headers import *
from pages.tools_page import (ToolsPage)
from utils.browser_utils import (BrowserUtils)

# PHC-TS04-TC001: 세부 특기사항 탭 이동 테스트
def test_go_to_special_note(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    assert tools_page.is_special_note_page(), "세부특기사항 탭으로 이동 실패"
    print("PHC-TS04-TC001 : Test success")    
    
# PHC-TS04-TC002: 정보 입력 및 결과 출력 확인
def test_input_info_result(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    tools_page.select_school_class("초등")
    tools_page.select_subject("초등","국어")
    
    file_path = os.path.abspath("src/resources/assets/test_student_evaluation_template.xlsx")
    tools_page.upload_data(file_path)
    
    tools_page.click_auto_create_button()
    #WebDriverWait #생성결과 다운받기 버튼이 화면에 표시될 때 까지
       