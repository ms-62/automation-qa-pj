import os
import pytest

from utils.headers import *
from pages.tools_page import (ToolsPage)
from utils.browser_utils import (BrowserUtils)
from utils.defines import NAME,XPATH,SELECTORS,TARGET_URL
from utils.download_utils import wait_for_download, wait_for_download_contains

from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult
from utils.defines import TestResult

from utils.browser_setup import create_driver  # ✅ 추가
from pages.login_page import LoginPage         # ✅ 추가
from pages.main_page import MainPage           # ✅ 추가
from pages.member_page import MemberPage       # ✅ 추가
from pages.agent_page import AgentPage         # ✅ 추가
from managers.file_manager import FileManager  # ✅ fm fixture가 이 파일에 없으면 필요
from utils.context import LoginContext         # ✅ logged_in_agent에서 필요

# ✅ 이 파일(test_tools.py)에서만: 테스트마다 새 브라우저
@pytest.fixture(scope="function")
def driver():
    driver = create_driver()
    yield driver
    driver.quit()

# ✅ fm fixture가 conftest에 있으면 없어도 되는데,
#    "이 파일만 단독으로 돌려도 되게" 하려면 넣어두는게 안전
@pytest.fixture
def fm():
    return FileManager()

# ✅ tools_page도 이 파일에서만 새 driver를 쓰도록 오버라이드
@pytest.fixture
def tools_page(driver):
    return ToolsPage(driver)

# ✅ user_data fixture가 conftest에 이미 있으면 여기서 정의 안 해도 됨
#    (만약 test_tools.py 단독 실행 시 user_data가 없다고 뜨면 아래 주석 해제)
# @pytest.fixture
# def user_data(fm):
#     return fm.read_json_file("user_data.json")

# ✅ 이 파일(test_tools.py)에서만: 같은 driver로 로그인 보장
@pytest.fixture
def logged_in_agent(driver, fm, user_data):
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    member_page = MemberPage(driver)
    agent_page = AgentPage(driver)

    ctx = LoginContext(
        driver=driver,
        fm=fm,
        login_page=login_page,
        main_page=main_page,
        member_page=member_page,
        agent_page=agent_page,
        user_data=user_data
    )

    browser_utils = BrowserUtils()

    # 쿠키로 빠른 로그인 시도
    browser_utils.load_cookies(
        driver=driver,
        fm=fm,
        url=TARGET_URL["MAIN_URL"],
        file_name="cookies.json"
    )

    driver.get(TARGET_URL["MAIN_URL"])
    driver.refresh()
    time.sleep(0.5)

    if not browser_utils.is_logged_in(driver):
        browser_utils.auto_login(ctx)

    return agent_page


# # PHC-TS04-TC001: 세부 특기사항 탭 이동 테스트
# def test_go_to_special_note(logged_in_agent,tools_page, fm):
#     test_name = "test_go_to_special_note"
#     ctx = TextContext(test_name, page="tools_page")
#     start = time.perf_counter()
    
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     assert tools_page.is_special_note_page(), "세부특기사항 탭으로 이동 실패"
#     log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_success"))    
    
# PHC-TS04-TC002~TC004
# def test_input_info_result(logged_in_agent,tools_page):
#     # PHC-TS04-TC002: 정보 입력 및 결과 출력 확인
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     tools_page.select_subject("초등","영어")
    
#     file_path = os.path.abspath("src/resources/assets/test_student_evaluation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         # PHC-TS04-TC003: 다시 생성 후 다시 생성 버튼 동작
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )
    
#     # PHC-TS04-TC004: 생성 결과 다운받기 버튼 확인  
#     WebDriverWait(tools_page.driver, 10).until(
#     EC.element_to_be_clickable(
#         (By.XPATH, XPATH["BTN_DOWNLOAD_RESULT"])
#         )
#     )
#     tools_page.click_download_result_button()
#     # 다운로드 확인 메서드
#     download_dir = "src/resources/downloads"
#     downloaded = wait_for_download_contains(download_dir, ext=".xlsx", timeout=30)
#     assert downloaded is not None, "다운로드가 안됨"
    
# # PHC-TS04-TC005 : 생성 이후 중지 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     tools_page.select_subject("중등","정보")
    
#     file_path = os.path.abspath("src/resources/assets/test_student_evaluation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )
        
#     tools_page.click_create_abort_button()
#     assert tools_page.is_create_abort_page(), "생성 중지에 실패했습니다."

# # PHC-TS04-TC006 : 다시 생성 이후 취소 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     tools_page.select_subject("고등","한국사")
    
#     file_path = os.path.abspath("src/resources/assets/test_student_evaluation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
    
#     tools_page.click_create_reject_button()
#     assert not tools_page.is_recreate_modal_open(), "취소 버튼이 동작하지 않습니다."

# # PHC-TS04-TC007: 지원되지 않는 파일 형식 업로드
# def test_not_supported_file_upload(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     file_path = os.path.abspath("src/resources/assets/test_pdf.pdf")
#     tools_page.upload_file(file_path)
#     assert not tools_page.get_upload_error_text(), "파일 형식 오류 시 응답메시지 없음"

# # PHC-TS04-TC009: 입력 양식 다운받기 버튼 테스트
# def test_file_download_button_test(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     tools_page.click_download_template()
    
#     # 다운로드 확인 메서드
#     download_dir = "src/resources/downloads"
#     assert wait_for_download(download_dir, "student_evaluation_template")
    
# # PHC-TS04-TC010: 성취기준 검색하기 URL 이동 확인
# def test_go_to_achievement_page(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_special_note_page()
#     tools_page.click_achievement_button()
#     tools_page.switch_to_new_tab()
#     assert tools_page.is_achievement_page(), "페이지 이동 안됨"


####################################################
# 행동특성 및 종합의견  
# PHC-TS04-TC011: 행동특성 및 종합의견 탭 이동
# def test_go_to_opinion(logged_in_agent,tools_page, fm):
#     test_name = "go_to_special_note_test"
#     ctx = TextContext(test_name, page="tools_page")
#     start = time.perf_counter()

#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     assert tools_page.is_opinion_note_page(), "행동특성 탭으로 이동 실패"
#     log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_success"))    

# # PHC-TS04-TC015~TC017
# def test_input_info_result(logged_in_agent,tools_page):
#     # PHC-TS04-TC015: 정보 입력 및 결과 출력 확인
#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     file_path = os.path.abspath("src/resources/assets/student_record_generation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         # PHC-TS04-TC016: 다시 생성 후 다시 생성 버튼 확인
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )
#     # PHC-TS04-TC017: 생성 결과 다운받기 버튼 확인  
#     WebDriverWait(tools_page.driver, 20).until(
#     EC.element_to_be_clickable(
#         (By.XPATH, XPATH["BTN_DOWNLOAD_RESULT"])
#         )
#     )
#     tools_page.click_download_result_button()
#     # 다운로드 확인 메서드
#     download_dir = "src/resources/downloads"
#     downloaded = wait_for_download_contains(download_dir, ext=".xlsx", timeout=30)
#     assert downloaded is not None, "다운로드가 안됨"

# # PHC-TS04-TC018 : 생성 이후 중지 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     file_path = os.path.abspath("src/resources/assets/student_record_generation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )
        
#     tools_page.click_create_abort_button()
#     assert tools_page.is_create_abort_page(), "생성 중지에 실패했습니다."

# # PHC-TS04-TC019 : 다시 생성 이후 취소 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     file_path = os.path.abspath("src/resources/assets/student_record_generation_template.xlsx")
#     tools_page.upload_file(file_path)
#     assert tools_page.is_valid_upload_file(), "파일 업로드 실패"
#     tools_page.input_teacher_comment("AI가 세부 특기사항 작성 시 반영할 사항이나 고려할 점을 알려주세요")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
    
#     tools_page.click_create_reject_button()
#     assert not tools_page.is_recreate_modal_open(), "취소 버튼이 동작하지 않습니다."

# # PHC-TS04-TC020: 지원되지 않는 파일 형식 업로드
# def test_not_supported_file_upload(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     file_path = os.path.abspath("src/resources/assets/test_pdf.pdf")
#     tools_page.upload_file(file_path)
#     assert not tools_page.get_upload_error_text(), "파일 형식 오류 시 응답메시지 없음"

# # PHC-TS04-TC022: 입력 양식 다운 받기 버튼 확인
# def test_opinion_file_download_button_test(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_opinion_note_page()
#     tools_page.click_download_template()
    
#     # 다운로드 확인 메서드
#     download_dir = "src/resources/downloads"
#     assert wait_for_download(download_dir, "student_record_generation_template")


####################################################
## 수업지도안 
# # PHC-TS04-TC023: 수업지도안 탭 이동
# def test_go_to_teaching(logged_in_agent,tools_page, fm):
#     test_name = "test_go_to_teaching_note"
#     ctx = TextContext(test_name, page="tools_page")
#     start = time.perf_counter()

#     tools_page.go_to_tools_page()
#     tools_page.click_teaching_note_page()
#     assert tools_page.is_teaching_note_page(), "수업지도안 탭으로 이동 실패"
#     log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_success"))    

# PHC-TS04-TC024~TC025
# def test_input_info_result(logged_in_agent,tools_page):
#     # PHC-TS04-TC024: 정보 입력 및 결과 출력 확인
#     tools_page.go_to_tools_page()
#     tools_page.click_teaching_note_page()
#     tools_page.input_information("초등","6학년","실과","40분")
#     tools_page.input_achievement_standard("[2국06-02]")
#     tools_page.input_teacher_comment("AI가 수업 지도안 작성 시 반영할 사항이나 고려할 점을 알려주세요.")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         # PHC-TS04-TC025: 다시 생성 후 다시 생성 버튼 확인
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )
    
#     WebDriverWait(tools_page.driver, 20).until(
#     EC.presence_of_element_located(
#         (By.XPATH, XPATH["TEACHING_RESULT_VALID"])
#         )
#     )
#     assert not tools_page.is_teaching_result_valid(), "생성 결과가 출력되지 않습니다."

# # PHC-TS04-TC026: 다시 생성 후 취소 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_teaching_note_page()
#     tools_page.input_information("고등","1학년","제2외국어/한문","50분")
#     tools_page.input_achievement_standard("[2국06-02]")
#     tools_page.input_teacher_comment("AI가 수업 지도안 작성 시 반영할 사항이나 고려할 점을 알려주세요.")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
#     tools_page.click_create_reject_button()
#     assert not tools_page.is_recreate_modal_open(), "취소 버튼이 동작하지 않습니다."

# # PHC-TS04-TC027: 생성 중 중지 버튼 확인
# def test_input_info_result(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_teaching_note_page()
#     tools_page.input_information("중등","2학년","정보","45분")
#     tools_page.input_achievement_standard("[2국06-02]")
#     tools_page.input_teacher_comment("AI가 수업 지도안 작성 시 반영할 사항이나 고려할 점을 알려주세요.")
    
#     try:
#         tools_page.click_auto_create_button()
#     except:
#         tools_page.click_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, XPATH["BTN_SURE_RECREATE"]))
#         )
        
#         tools_page.click_sure_recreate_button()
#         WebDriverWait(tools_page.driver, 10).until(
#             EC.invisibility_of_element_located(
#                 (By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])
#             )
#         )

#     tools_page.click_create_abort_button()
#     assert tools_page.is_create_abort_page(), "생성 중지에 실패했습니다."

# # PHC-TS04-TC028: 성취 기준 검색하기 URL 이동 확인
# def test_go_to_achievement_page(logged_in_agent,tools_page):
#     tools_page.go_to_tools_page()
#     tools_page.click_teaching_note_page()
#     tools_page.click_achievement_button()
#     tools_page.switch_to_new_tab()
#     assert tools_page.is_achievement_page(), "페이지 이동 안됨"

####################################################
# PHC-TS04-TC023: PPT 생성 탭 이동


# PHC-TS04-TC024: 정보 입력 및 결과 출력 확인


# PHC-TS04-TC025: 
