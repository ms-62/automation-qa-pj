from utils.headers import *

from pages.model_setting_page import ModelSettingPage

from utils.defines import DEFAULT_MODEL
from utils.defines import ChatKey, ChatType, TestResult, ChatMenu

from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult


# main 홈화면 테스트만 진행합니다. 
# ======================== E2E - AI 대화 시나리오 ==============================  
def test_conversation_scenario(logged_in_main, fm):
    page = logged_in_main
    
    test_name = "test_conversation_scenario"
    ctx = TextContext(test_name, page="chat")
    start = time.perf_counter()
    try:
        page.click_btn_home_menu(ChatMenu.DEFAULT_CHAT)
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_btn_home_menu"))

        result = TestResult.PASSED if page.compare_chats_after_user_send() else TestResult.FAILED
        log_action(ctx, ActionResult(test_name, result, elapsed_time = 0, detail = "action_user_chat"))

        # 사용자의 질문 내용이 저장된 후 클립보드에 복사되는지 검사
        
            
        page.click_btn_retry()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_btn_retry"))

        page.copy_last_response()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "copy_last_response"))

        page.paste_last_response()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "paste_last_response"))

        page.reset_chat()
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "test_conversation_scenario_ended"))
        
    except:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))


#     # 사용자가 보낸 메시지 내용 편집
#     # 사용자가 보낸 메시지 내용 편집 중 취소
#     # 사용자가 보낸 메시지 복사  

    
# # ====================== 스크롤  ============================== 
# def test_chat_scroll(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_chat_scroll"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.select_latest_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "select_latest_chat"))

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

# ======================= 검색 ==========================
# def test_search_chat(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_search_chat"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         result = TestResult.PASSED if page.click_btn_home_menu(ChatMenu.SEARCH_CHAT) else TestResult.FAILED
#         log_action(ctx, ActionResult(test_name, result, elapsed_time = 0, detail = "click_btn_search_menu"))

#         page.search_past_chats_by_click()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "search_past_chats_by_click"))        
        
#         result = TestResult.PASSED if page.click_btn_home_menu(ChatMenu.SEARCH_CHAT) else TestResult.FAILED
#         log_action(ctx, ActionResult(test_name, result, elapsed_time = 0, detail = "click_btn_search_menu"))
        
#         result = TestResult.PASSED if page.search_past_chats_by_input() else TestResult.FAILED
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "test_search_chat_ended"))  
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))


    
# ======================== E2E - 기존 대화 시나리오 ==============================  
# def test_past_chats_scenario(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_past_chats_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.select_latest_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "set_current_chat"))
        
#         page.scroll_down_past_chats()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "scroll_down_past_chats"))
        
#         page.scroll_up_past_chats()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "scroll_up_past_chats"))

#         result = TestResult.PASSED if page.rename_chat() else TestResult.FAILED
#         log_action(ctx, ActionResult(test_name, result, elapsed_time = 0, detail = "rename_chat"))

#         result = TestResult.PASSED if page.delete_chat() else TestResult.FAILED
#         log_action(ctx, ActionResult(test_name, result, elapsed_time = 0, detail = "delete_chat"))
        
#         page.cancel_edit()
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "cancel_edit"))
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
# def test_cancel_past_edit(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_cancel_past_edit"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:        
#         page.select_latest_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "select_latest_chat"))
        
#         page.open_selected_edit_menu()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "open_selected_edit_menu"))
        
#         page.click_change_chat_name()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_change_chat_name"))
        
#         page.click_cancel_edit()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_cancel_edit"))
        
#         page.open_selected_edit_menu()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "open_selected_edit_menu"))
        
#         page.click_delete_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_delete_chat"))
        
#         page.click_cancel_edit()
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "PHC-TS03-TC022 PHC-TS03-TC024 ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
# def test_rename_past_chat(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_rename_chat"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
    
#     page.select_latest_chat()
#     log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "select_latest_chat"))
    
#     elapsed = time.perf_counter() - start
#     result = TestResult.PASSED if page.rename_chat() else TestResult.FAILED
#     log_action(ctx, ActionResult(test_name, result, elapsed, detail = "PHC-TS03-TC021 ended"))


# def test_delete_past_chat(logged_in_main, fm):
#     page = logged_in_main
    
#     test_name = "test_delete_chat"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:    
#         prev_len = len(page.get_all_chats())

#         page.select_latest_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "select_latest_chat"))
    
#         page.open_selected_edit_menu()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "open_selected_edit_menu"))
        
#         page.click_delete_chat()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_delete_chat"))
        
#         page.click_delete_confirm()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time = 0, detail = "click_delete_confirm"))
#         after_len = len(page.get_all_chats())
        
#         result = False if prev_len == after_len else True
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, result, elapsed, detail = "PHC-TS03-TC023 ended"))
#     except:
#         elapsed = time.perf_counter() - start
#         fm.save_screenshot_png(page.driver, test_name)
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))


# ====================== 이미지 생성 요청 ============================== 
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
        
# ====================== 웹 검색 요청 ============================== 
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


# ====================== E2E 파일 업로드 ============================== 
# def test_file_upload_scenario(logged_in_main, fm):
#     page = logged_in_main

#     test_name = "test_file_upload_scenario"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         page.upload_files()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail="upload_files"))
        
#         page.upload_multi_files()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail="upload_multi_files"))
        
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
    
    
# ======================== E2E - AI 모델 활성화 테스트 ============================== 
# def test_model_scenario(logged_in_main, driver):
#     page = logged_in_main
    
#     model_page = ModelSettingPage(driver)
    
#     test_name = "test_model_setting"
#     ctx = TextContext(test_name, page="chat")
#     start = time.perf_counter()
#     try:
#         model_page.open_model_menu()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_model_menu"))

#         model_page.select_last_model()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "select_last_model"))

#         model_page.open_model_menu()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_model_menu"))

#         model_page.go_to_model_setting()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "go_to_model_setting"))

#         model_page.toggle_all_models_and_verify()        
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "toggle_all_models_and_verify"))

#         model_page.go_back() # 설정창 닫기
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "go_back"))

#         model_page.compare_active_models()  # 드롭다운 검증
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "compare_active_models"))

#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed, detail = "test_model_scenario_ended"))
        
#     except:
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
