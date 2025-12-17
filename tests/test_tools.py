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
    
    tools_page.input_add_data("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
    tools_page.click_auto_create_button()
    #WebDriverWait #생성결과 다운받기 버튼이 화면에 표시될 때 까지
    tools_page.click_download_result_button()


# PHC-TS04-TC003: 지원되지 않는 파일 형식 업로드
def test_not_supported_file_upload(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    file_path = os.path.abspath("src/resources/assets/test_pdf.pdf")
    tools_page.upload_data(file_path)
    assert tools_page.is_upload_error_visible(), "에러 출력 오류"
    assert tools_page.get_upload_error_text(" "), "메시지 출력 오류"
    
# PHC-TS04-TC004: 대용량 파일 업로드
def test_big_file_upload(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    file_path = os.path.abspath("   ")
    tools_page.upload_data(file_path)
    assert tools_page.is_upload_error_visible(), "에러 출력 오류"
    assert tools_page.get_upload_error_text(" "), "메시지 출력 오류"

# PHC-TS04-TC005: 입력 양식 다운받기 버튼 테스트
def test_file_download_button_test(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    tools_page.click_download_template()
    # 다운로드 확인 메서드
    
# PHC-TS04-TC006: 입력 양식 다운받기 버튼 테스트
def test_go_to_achievement_page(logged_in_agent,tools_page):
    tools_page.go_to_tools_page()
    tools_page.click_special_note_page()
    tools_page.click_achievement_button()
    tools_page.switch_to_new_tab()
    assert tools_page.is_achievement_page(), "페이지 이동 안됨"