from utils.headers import *

from pages.model_setting_page import ModelSettingPage
from pages.past_chats_page import PastChatsPage

from utils.defines import DEFAULT_MODEL, DEFAULT_CHAT
from utils.defines import ChatKey, ChatType, TestResult

from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult


# main 홈화면 테스트만 진행합니다. 
# # ====================== 대화  ============================== 
# def test_conversation_scenario(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_conversation_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.click_btn_home_menu(DEFAULT_CHAT)
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_btn_home_menu"))

#         page.action_user_chat(ChatKey.INPUTS, ChatType.TEXT)
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "action_user_chat"))

#         page.click_btn_retry()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_btn_retry"))

#         page.copy_last_response()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "copy_last_response"))

#         page.paste_last_response()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "paste_last_response"))

#         page.reset_chat()
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "test_conversation_scenario_ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
    
# # ====================== 스크롤  ============================== 
# def test_chat_scroll(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_chat_scroll"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.click_on_past_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_on_past_chat"))

#         # 아래 스크롤 버튼
#         page.click_btn_scroll_to_bottom()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_btn_scroll_to_bottom"))

#         # 스크롤 업
#         up_result = page.scroll_up_chat()
#         log_action(ctx, up_result, target="chat_area")
#         assert up_result.result == TestResult.PASSED

#         # 스크롤 다운
#         down_result = page.scroll_down_chat()
#         log_action(ctx, down_result, target="chat_area")
#         assert down_result.result == TestResult.PASSED
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))


#     # 사용자가 보낸 메시지 내용 편집
#     # 사용자가 보낸 메시지 내용 편집 중 취소
#     # 사용자가 보낸 메시지 복사  
    
    
# # def test_past_chats(logged_in_main):
# #     page = logged_in_main
    
# #     past_chat_page = PastChatsPage(driver)
  
#     # 이름변경' 버튼 동작
#     # 이름 변경 '취소' 버튼 동작
#     # 삭제' 버튼 동작

# # ====================== 이미지 생성 요청 ============================== 
# def test_gen_image_scenario(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_gen_image_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.action_gen_image()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail="gen_image_btn"))

#         page.action_user_chat(ChatKey.REQUESTS, ChatType.IMAGE_REQUEST)
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail="request_img"))

#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail="test_gen_image_scenario ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
# # ====================== 웹 검색 요청 ============================== 
# def test_web_sarch_scenario(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_web_sarch_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.action_search_web()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail="action_search_web"))

#         page.action_user_chat(ChatKey.REQUESTS, ChatType.WEB_REQUEST)
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail="request_websearch"))

#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail="test_web_sarch_scenario ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))


# # ====================== 파일 업로드 ============================== 
# def test_file_upload_scenario(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_file_upload_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.upload_files()
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail="test_file_upload_scenario ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
# # ====================== 메뉴 테스트 ============================== 
# def test_menu_scenario(logged_in_main):
#     page = logged_in_main
    
#     test_name = "test_menu_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.sync_menu_status()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "sync_menu_status"))

#         page.action_menu_arrow()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "action_menu_arrow"))

#         page.action_menu_bar()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "action_menu_bar"))

#         page.action_menu_bar()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "action_menu_bar"))

#         page.action_menu_arrow()
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= elapsed, detail="test_menu_scenario ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed_time = elapsed))
    
    
# ======================== AI 모델 활성화 테스트 ============================== 
# E2E 

def test_model_scenario(logged_in_main, driver):
    page = logged_in_main
    
    model_page = ModelSettingPage(driver)
    
    test_name = "test_model_setting"
    ctx = TextContext(test_name, page="chat")
    start = time.perf_counter()
    try:
        model_page.open_model_menu()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_model_menu"))

        model_page.select_last_model()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "select_last_model"))

        model_page.open_model_menu()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_model_menu"))

        model_page.go_to_model_setting()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "go_to_model_setting"))

        model_page.toggle_all_models_and_verify()        
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "toggle_all_models_and_verify"))

        model_page.go_back() # 설정창 닫기
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "go_back"))

        model_page.compare_active_models()  # 드롭다운 검증
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "compare_active_models"))

        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "test_model_scenario_ended"))
        
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
