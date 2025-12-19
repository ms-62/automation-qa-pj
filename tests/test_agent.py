from utils.headers import *
from enums.ui_status import AIresponse
import re

from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult
from utils.defines import TestResult

# PHC-TS06-TC001
def test_search_agent_list(logged_in_agent, fm):
    test_name = "agent_search_test"
    ctx = TextContext(test_name, page="agent_search")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.search_input("project")
        result = agent_page.search_result()
        fail_result = agent_page.search_no_result()
        assert fail_result is None, "PHC-TS06-TC001 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "search_existed_agent"))
        
        assert "project" in result.text.strip(), "PHC-TS06-TC001 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "search_existed_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC002
def test_search_agent_fail(logged_in_agent,fm) :
    test_name = "agent_search_test"
    ctx = TextContext(test_name, page="agent_search")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.search_input("마라탕")
        result = agent_page.search_no_result()
        assert result, "PHC-TS06-TC002 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "search_not_existed_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
   
# PHC-TS06-TC003
def test_agent_talk_card(logged_in_agent, fm) :
    test_name = "agent_chat_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        element_text = agent_page.agent_talk_card_text().text.strip()
        agent_page.agent_talk_card_click()
        agent_page.scroll_up_chat()
        my_text = agent_page.check_my_talk_input().text.strip()
        assert element_text == my_text, "PHC-TS06-TC003 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "chat_agent_with_card"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC004
def test_agent_talk_response_complete(logged_in_agent, fm) :
    test_name = "agent_chat_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        question = data["inputs"][0]["content"]
        result = agent_page.ai_chat_complete(question)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC004 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC005   
def test_agent_talk_response_stop(logged_in_agent, fm) :
    test_name = "agent_chat_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        question = data["inputs"][0]["content"]
        result = agent_page.input_chat_stop(question)
        assert result == AIresponse.STOPPED, "PHC-TS06-TC005 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response_when_stop"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC006
def test_agent_talk_create_again(logged_in_agent, fm) :
    test_name = "agent_chat_create_again_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        question = data["inputs"][0]["content"]
        result = agent_page.ai_chat_complete(question)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC006 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
        
        again_result = agent_page.create_again_response()
        assert again_result == AIresponse.COMPLETED, "PHC-TS06-TC006 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response_when_create_again"))
        
        element = agent_page.check_create_again_response()
        assert element is not None, "PHC-TS06-TC006 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "check_create_again_element"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
  
# PHC-TS06-TC009  
def test_agent_talk_copy_and_paste(logged_in_agent, fm) :
    test_name = "agent_chat_copy_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        question = data["inputs"][0]["content"]
        result = agent_page.ai_chat_complete(question)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC009 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
        
        copy_text = agent_page.copy_last_response()
        agent_page.paste_last_response()
        paste_text = agent_page.check_paste()
        def normalize_text(text: str) -> str:
            return re.sub(r'\s+', ' ', text).strip()
        assert normalize_text(copy_text) in normalize_text(paste_text), "PHC-TS06-TC009 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response_copy"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC011
def test_agent_talk_file_upload(logged_in_agent, fm) :
    test_name = "agent_chat_upload_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_file_in_chat()
        element = agent_page.check_file_upload_in_chat()
        assert element, "PHC-TS06-TC011 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_file_in_chat"))
        
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC011 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC012
def test_agent_talk_img_upload(logged_in_agent, fm) :
    test_name = "agent_chat_upload_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_img_in_chat()
        element = agent_page.check_img_upload_in_chat()
        assert element, "PHC-TS06-TC011 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_img_in_chat"))
        
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC012 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC013
def test_agent_talk_expand_downsize_img(logged_in_agent, fm) :
    test_name = "agent_chat_img_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_img_in_chat()
        element = agent_page.check_img_upload_in_chat()
        assert element, "PHC-TS06-TC013 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_img_in_chat"))
        
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC013 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
        
        result = agent_page.expand_img_in_chat()
        assert result is True, "PHC-TS06-TC013 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "expand_img"))
        
        element = agent_page.downsize_img_in_chat()
        assert element is None, "PHC-TS06-TC013 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "downsize_img"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC014
def test_agent_talk_upload_and_delete(logged_in_agent, fm) :
    test_name = "agent_chat_delete_file_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_file_in_chat()
        element = agent_page.check_file_upload_in_chat()
        assert element, "PHC-TS06-TC014 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_file_in_textarea"))
        
        agent_page.delete_file_in_chat()
        element = agent_page.check_file_upload_in_chat()
        assert element is None, "PHC-TS06-TC014 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "delete_file_in_textarea"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC015
def test_agent_talk_download_img(logged_in_agent, fm) :
    test_name = "agent_chat_download_img_option_test"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_img_in_chat()
        element = agent_page.check_img_upload_in_chat()
        assert element, "PHC-TS06-TC015 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_img_in_chat"))
        
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC015 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
        
        result = agent_page.download_img_in_chat()
        assert result is True, "PHC-TS06-TC015 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "download_img"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC017
def test_agent_talk_big_file_upload(logged_in_agent, fm) :
    test_name = "agent_chat_exception_test_upload_big_file"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try: 
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_big_file_in_chat()
        element = agent_page.check_file_upload_in_chat()
        assert element, "PHC-TS06-TC017 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_big_file_in_chat"))
        
        loading = agent_page.wait_until_loading_disappear()
        assert loading is True, "PHC-TS06-TC017 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "wait_until_loading_disappeared"))
        
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC017 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC018
def test_agent_talk_upload_exe_to_file(logged_in_agent, fm) :
    test_name = "agent_chat_exception_test_upload_exe_file"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.open_upload_file_dialog()
        agent_page.upload_exe_file_in_chat()
        element = agent_page.check_file_upload_in_chat()
        assert element is None, "PHC-TS06-TC018 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_when_upload_exe"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC019
def test_agent_upload_many_files(logged_in_agent, fm) :
    test_name = "agent_chat_exception_test_upload_many_files"
    ctx = TextContext(test_name, page="agent_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.talk_with_agent_screen()
        agent_page.upload_files_in_chat()
        result = agent_page.ai_chat_complete("")
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC019 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "agent_response_when_upload_20up_files"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC022
def test_make_agent_chat_stop(logged_in_agent, fm) :
    test_name = "chat_stop_test_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.go_to_make_chat()
        data = fm.read_json_file("agent_text_data.json")
        input = data["chat_make_input"][0]["content"]
        result = agent_page.chatmake_input_chat_stop(input)
        assert result == AIresponse.STOPPED, "PHC-TS06-TC022 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response_stop"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC023
def test_make_agent_chat_create_again(logged_in_agent, fm) :
    test_name = "chat_create_again_option_test_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_chat")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.go_to_make_chat()
        data = fm.read_json_file("agent_text_data.json")
        input = data["chat_make_input"][0]["content"]
        result = agent_page.chatmake_input_chat(input)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC023 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response"))
        
        agent_page.chatmake_create_again_response()
        element = agent_page.check_chatmake_create_again_response()
        assert element is not None, "PHC-TS06-TC023 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "create_again_ai_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC026
def test_make_agent_chat_copy_and_paste(logged_in_agent, fm) :
    test_name = "chat_copy_option_test_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.go_to_make_chat()
        data = fm.read_json_file("agent_text_data.json")
        input = data["chat_make_input"][0]["content"]
        result = agent_page.chatmake_input_chat(input)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC026 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response"))
        
        agent_page.copy_last_response_in_chatmake()
        agent_page.paste_last_response_in_chatmake()
        paste_text = agent_page.check_paste_in_chatmake()
        assert len(paste_text) > 0, "PHC-TS06-TC026 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "copy_ai_response"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC028
def test_make_agent_setting_for_me(logged_in_agent, fm) :
    test_name = "make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        check = agent_page.make_agent_for_me().text.strip()
        assert "나만보기" in check, "PHC-TS06-TC028 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_for_me"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC029
def test_make_agent_setting_for_agency(logged_in_agent, fm) :
    test_name = "make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        check = agent_page.make_agent_for_agency().text.strip()
        assert "기관 공개" in check, "PHC-TS06-TC029 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_for_organization"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC030  
def test_make_agent_setting_no_name(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try:
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input("")
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        btn = agent_page.check_btn_disabled()
        error = agent_page.error_message().text.strip()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC030 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_no_name"))
        
        assert "이름" in error, "PHC-TS06-TC030 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_make_agent_with_no_name"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC031 
def test_make_agent_setting_long_name(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["over_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        btn = agent_page.check_btn_disabled()
        error = agent_page.error_message().text.strip()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC031 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_long_name"))
        
        assert "이름" in error, "PHC-TS06-TC031 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_make_agent_with_long_name"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC032 
def test_make_agent_setting_no_intro(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input("")
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        time.sleep(3)
        btn = agent_page.check_btn_disabled()
        assert btn.get_attribute("disabled") is None, "PHC-TS06-TC032 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_no_intro"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC033
def test_make_agent_setting_long_intro(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["over_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        btn = agent_page.check_btn_disabled()
        error = agent_page.error_message().text.strip()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC033 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_long_intro"))
        
        assert "한줄" in error, "PHC-TS06-TC033 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_make_agent_with_long_intro"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC034  
def test_make_agent_setting_no_rule(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input("")
        agent_page.setting_card_input(card)
        btn = agent_page.check_btn_disabled()
        error = agent_page.error_message().text.strip()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC034 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_no_rule"))
        
        assert "규칙" in error, "PHC-TS06-TC034 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_make_agent_with_no_rule"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC035  
def test_make_agent_setting_long_rule(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["over_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        time.sleep(3)
        btn = agent_page.check_btn_disabled()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC035 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_long_rule"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC036  
def test_make_agent_setting_delete_card(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_card_input(card)
        before_btns = agent_page.check_card_number()
        assert len(before_btns) == 3, "PHC-TS06-TC036 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "before_delete_card_input"))
        
        agent_page.delete_card()
        after_btns = agent_page.check_card_number()
        assert len(after_btns) == 2, "PHC-TS06-TC036 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "delete_card_input"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC037 
def test_make_agent_setting_no_card(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input("")
        time.sleep(3)
        btn = agent_page.check_btn_disabled()
        assert btn.get_attribute("disabled") is None, "PHC-TS06-TC037 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_no_card"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC038 
def test_make_agent_setting_long_card(logged_in_agent, fm) :
    test_name = "make_agent_exception_test"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["over_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        time.sleep(3)
        btn = agent_page.check_btn_disabled()
        assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC038 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_long_card"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC039
def test_make_agent_setting_many_option(logged_in_agent, fm) :
    test_name = "duplicate_check_option_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        intro = data["setting_inputs"][1]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_intro_input(intro)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        agent_page.scroll_down_setting()
        agent_page.multi_function()
        btn = agent_page.check_btn_disabled()
        assert btn.get_attribute("disabled") is None, "PHC-TS06-TC039 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_agent_with_duplicate_check_option"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC040
def test_make_agent_image_upload(logged_in_agent, fm):
    test_name = "img_upload_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.upload_image("test_asset.jpg")
        uploaded = agent_page.check_upload_image(3)
        assert uploaded.is_displayed(), "PHC-TS06-TC040 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_img"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC041
def test_make_agent_big_image_upload(logged_in_agent, fm):
    test_name = "big_img_upload_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.upload_image("test_big_img.tif")
        assert agent_page.check_upload_big_img(), "PHC-TS06-TC041 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_big_img"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC042
def test_make_agent_exe_to_img_upload(logged_in_agent,fm):
    test_name = "exe_upload_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        agent_page.upload_image("test_exe.exe")
        error = agent_page.error_message()
        uploaded = agent_page.check_upload_image(3)
        assert uploaded is None, "PHC-TS06-TC042 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_exe_file"))
        
        assert error is not None, "PHC-TS06-TC042 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_when_upload_exe"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC043
def test_make_agent_make_image(logged_in_agent, fm) :
    test_name = "make_img_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        time.sleep(3)
        agent_page.make_image()
        uploaded = agent_page.check_upload_image(10)
        assert uploaded.is_displayed(), "PHC-TS06-TC043 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "make_img_option_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC044
def test_make_agent_file_upload(logged_in_agent, fm) :
    test_name = "file_upload_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_file("test_pdf.pdf")
        uploaded = agent_page.check_upload_file()
        assert uploaded, "PHC-TS06-TC044 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_file_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC045
def test_make_agent_upload_img_to_file(logged_in_agent, fm) :
    test_name = "upload_img_to_file_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_file("test_asset.jpg")
        uploaded = agent_page.check_upload_file()
        assert uploaded, "PHC-TS06-TC045 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_img_to_file_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC046
def test_make_agent_upload_big_file(logged_in_agent, fm) :
    test_name = "upload_big_file_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_file("big_file.md")
        uploaded = agent_page.check_fail_file_upload()
        assert uploaded, "PHC-TS06-TC046 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_big_file_in_make_agent"))
        
        msg = agent_page.check_fail_msg_file_upload()
        assert '크기' in msg.text.strip(), "PHC-TS06-TC046 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_upload_big_file_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC047
def test_make_agent_upload_exe_to_file(logged_in_agent, fm) :
    test_name = "upload_exe_to_img_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_file("test_exe.exe")
        uploaded = agent_page.check_fail_file_upload()
        assert uploaded, "PHC-TS06-TC047 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "upload_exe_to_img_in_make_agent"))
        
        msg = agent_page.check_fail_msg_file_upload()
        assert msg is not None, "PHC-TS06-TC047 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_upload_exe_to_img_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC048
def test_make_agent_upload_many_file(logged_in_agent, fm) :
    test_name = "upload_many_files_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_multiple_images(limit=21)
        error = agent_page.error_message().text.strip()
        assert "20개" in error, "PHC-TS06-TC048 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "error_msg_upload_many_files_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC049
def test_make_agent_delete_uploaded_file(logged_in_agent, fm) :
    test_name = "delete_file_in_make_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        agent_page.scroll_down_setting()
        agent_page.upload_file("test_asset.jpg")
        uploaded = agent_page.check_upload_file()
        if uploaded :
            agent_page.delete_for_uploaded_file()
        uploaded = agent_page.check_upload_file()
        assert uploaded is None, "PHC-TS06-TC049 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "delete_uploaded_file_in_make_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC051
def test_agent_back_while_make(logged_in_agent, fm) :
    test_name = "create_draft_agent"
    ctx = TextContext(test_name, page="make_agent_with_setting")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_my_agent()
        agent_page.make_agent_screen()
        agent_page.back_in_agent_make_screen()
        agent_page.driver.implicitly_wait(3)
        msg = agent_page.check_draft_msg()
        assert "초안" in msg.text.strip(), "PHC-TS06-TC051 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "create_draft_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC052
def test_agent_refresh_preview(logged_in_agent, fm) :
    test_name = "refresh_in_preview_chat"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["preview_inputs"][0]["content"]
        rule = data["preview_inputs"][1]["content"]
        input = data["preview_inputs"][2]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        agent_page.preview_input_chat(input)
        text = agent_page.preview_check_my_talk_input()
        assert text is not None, "PHC-TS06-TC052 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "before_refresh_preview_chat"))
        
        agent_page.refresh_btn_in_preview()
        element = agent_page.check_refresh_in_preview()
        assert element is not None, "PHC-TS06-TC052 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "after_refresh_preview_chat"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC053
def test_agent_chat_card_preview(logged_in_agent, fm) :
    test_name = "chat_in_preview"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        card = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        agent_page.setting_card_input(card)
        agent_page.preview_agent_talk_card_click()
        text = agent_page.preview_check_my_talk_input().text.strip()
        assert text in card, "PHC-TS06-TC053 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "card_chat_in_preview"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC054
def test_agent_chat_in_preview(logged_in_agent, fm) :
    test_name = "chat_in_preview"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        input = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        result = agent_page.preview_input_chat(input)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC054 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response_in_preview"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC055
def test_agent_stop_chat_in_preview(logged_in_agent, fm) :
    test_name = "chat_in_preview"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        input = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        result = agent_page.preview_input_chat_stop(input)
        assert result == AIresponse.STOPPED, "PHC-TS06-TC055 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_stop_response_in_preview"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC056
def test_agent_create_again_in_preview(logged_in_agent, fm) :
    test_name = "chat_option_in_preview"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        input = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        result = agent_page.preview_input_chat(input)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC056 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response_in_preview"))
        
        agent_page.preview_create_again_response()
        element = agent_page.check_preview_create_again_response()
        assert element is not None, "PHC-TS06-TC056 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "create_again_response_in_preview"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC059
def test_agent_copy_and_paste_in_preview(logged_in_agent, fm) :
    test_name = "chat_option_in_preview"
    ctx = TextContext(test_name, page="preview_chat")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.make_agent_screen()
        data = fm.read_json_file("agent_text_data.json")
        name = data["setting_inputs"][0]["content"]
        rule = data["setting_inputs"][2]["content"]
        input = data["setting_inputs"][3]["content"]
        agent_page.setting_name_input(name)
        agent_page.setting_rule_input(rule)
        result = agent_page.preview_input_chat(input)
        assert result == AIresponse.COMPLETED, "PHC-TS06-TC059 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "ai_response_in_preview"))
        
        copy_text = agent_page.copy_last_response_in_preview()
        agent_page.paste_last_response_in_preview()
        paste_text = agent_page.check_paste_in_preview()
        def normalize_text(text: str) -> str:
            return re.sub(r'\s+', ' ', text).strip()
        assert normalize_text(copy_text) in normalize_text(paste_text), "PHC-TS06-TC059 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "copy_response_in_preview"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC062
def test_modify_in_agents(logged_in_agent, fm) :
    test_name = "modify_agent_in_agent_search_screen"
    ctx = TextContext(test_name, page="modify_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_modify_in_agents()
        data = fm.read_json_file("agent_text_data.json")
        name = data["modify_inputs"][0]["content"]
        intro = data["modify_inputs"][1]["content"]
        rule = data["modify_inputs"][2]["content"]
        card = data["modify_inputs"][3]["content"]
        agent_page.modify_name(name)
        agent_page.modify_intro(intro)
        agent_page.modify_rule(rule)
        agent_page.modify_card(card)
        time.sleep(3)
        element = agent_page.modify_and_check()
        assert element is not None, "PHC-TS06-TC062 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "modify_agent_noti_display"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC064
def test_modify_in_my_agent(logged_in_agent, fm) :
    test_name = "modify_agent_in_my_agent_screen"
    ctx = TextContext(test_name, page="modify_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_my_agent()
        agent_page.go_to_modify_in_my_agent()
        data = fm.read_json_file("agent_text_data.json")
        name = data["modify_inputs"][0]["content"]
        intro = data["modify_inputs"][1]["content"]
        rule = data["modify_inputs"][2]["content"]
        card = data["modify_inputs"][3]["content"]
        agent_page.modify_name(name)
        agent_page.modify_intro(intro)
        agent_page.modify_rule(rule)
        agent_page.modify_card(card)
        time.sleep(3)
        element = agent_page.modify_and_check()
        assert element is not None, "PHC-TS06-TC064 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "modify_agent_noti_display"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS06-TC065
def test_not_delete_in_agents(logged_in_agent, fm) :
    test_name = "delete_agent_in_agent_search_screen"
    ctx = TextContext(test_name, page="delete_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_not_delete_in_agents()
        element = agent_page.check_delete_in_agents()
        assert element is None, "PHC-TS06-TC065 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "not_delete_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC066
def test_delete_in_agents(logged_in_agent, fm) :
    test_name = "delete_agent_in_agent_search_screen"
    ctx = TextContext(test_name, page="delete_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_delete_in_agents()
        element = agent_page.check_delete_in_agents()
        assert element is not None, "PHC-TS06-TC066 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "delete_agent_noti_display"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC067
def test_not_delete_in_my_agent(logged_in_agent, fm) :
    test_name = "delete_agent_in_my_agent_screen"
    ctx = TextContext(test_name, page="delete_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_my_agent()
        agent_page.go_to_not_delete_in_my_agent()
        element = agent_page.check_delete_in_my_agent()
        assert element is None, "PHC-TS06-TC067 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "not_delete_agent"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS06-TC068
def test_delete_in_my_agent(logged_in_agent, fm) :
    test_name = "delete_agent_in_my_agent_screen"
    ctx = TextContext(test_name, page="delete_agent")
    start = time.perf_counter()
    try :
        agent_page = logged_in_agent
        agent_page.go_to_agent_page()
        agent_page.go_to_my_agent()
        agent_page.go_to_delete_in_my_agent()
        element = agent_page.check_delete_in_my_agent()
        assert element is not None, "PHC-TS06-TC068 : Test Fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "delete_agent_noti_display"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(agent_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise