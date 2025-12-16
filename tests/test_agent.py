from utils.headers import *
from enums.ui_status import AIresponse

# PHC-TS06-TC001
# def test_search_agent_list(logged_in_agent):
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.search_input("project")
#     result = agent_page.search_result()
#     fail_result = agent_page.search_no_result()
    
#     assert fail_result is None, "PHC-TS06-TC001 : Test Fail"
#     assert "project" in result.text.strip(), "PHC-TS06-TC001 : Test Fail"
#     print("PHC-TS06-TC001 : Test Success")
    
# # PHC-TS06-TC002
# def test_search_agent_fail(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.search_input("마라탕")
#     result = agent_page.search_no_result()
    
#     assert result, "PHC-TS06-TC002 : Test Fail"
#     print("PHC-TS06-TC002 : Test Success")
   
# # PHC-TS06-TC003
# def test_agent_talk_card(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.talk_with_agent_screen()
#     element_text = agent_page.agent_talk_card_text().text.strip()
#     agent_page.agent_talk_card_click()
#     agent_page.scroll_up_chat()
#     my_text = agent_page.check_my_talk_input().text.strip()
    
#     assert element_text == my_text, "PHC-TS06-TC003 : Test Fail"
#     print("PHC-TS06-TC003 : Test Success")
    
# # PHC-TS06-TC004

# # PHC-TS06-TC005   
# def test_agent_talk_response_stop(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.talk_with_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     question = data["inputs"][0]["content"]
#     result = agent_page.input_chat_stop(question)
    
#     assert result == AIresponse.STOPPED, "PHC-TS06-TC005 : Test Fail"
#     print("PHC-TS06-TC005 : Test Success")

# PHC-TS06-TC011
def test_agent_talk_file_upload(logged_in_agent, fm) :
    agent_page = logged_in_agent
    agent_page.go_to_agent_page()
    agent_page.talk_with_agent_screen()
    agent_page.open_upload_file_dialog()
    agent_page.upload_file_in_chat()
    element = agent_page.check_file_upload_in_chat()
    assert element, "PHC-TS06-TC011 : Test Fail"
    result = agent_page.input_chat_stop("")
    assert result == AIresponse.STOPPED, "PHC-TS06-TC011 : Test Fail"
    print("PHC-TS06-TC011 : Test Success")
    
# # PHC-TS06-TC028
# def test_agent_setting_for_me(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     check = agent_page.make_agent_for_me().text.strip()
    
#     assert "나만보기" or "Private" in check, "PHC-TS06-TC028 : Test Fail"
#     print("PHC-TS06-TC028 : Test Success")
    
# # PHC-TS06-TC029
# def test_agent_setting_for_agency(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     check = agent_page.make_agent_for_agency().text.strip()
    
#     assert "기관 공개" or "Organization" in check, "PHC-TS06-TC029 : Test Fail"
#     print("PHC-TS06-TC029 : Test Success")

# # PHC-TS06-TC030  
# def test_agent_setting_no_name(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input("")
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     btn = agent_page.check_btn_disabled()
#     error = agent_page.error_message().text.strip()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC030 : Test Fail"
#     assert "이름" or "Name" in error, "PHC-TS06-TC030 : Test Fail"
#     print("PHC-TS06-TC030 : Test Success")

# # PHC-TS06-TC031 
# def test_agent_setting_long_name(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["over_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     btn = agent_page.check_btn_disabled()
#     error = agent_page.error_message().text.strip()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC031 : Test Fail"
#     assert "이름" or "Name" in error, "PHC-TS06-TC031 : Test Fail"
#     print("PHC-TS06-TC031 : Test Success")
    
# # PHC-TS06-TC032 
# def test_agent_setting_no_intro(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input("")
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     time.sleep(3)
#     btn = agent_page.check_btn_disabled()
    
#     assert btn.get_attribute("disabled") is None, "PHC-TS06-TC032 : Test Fail"
#     print("PHC-TS06-TC032 : Test Success")
    
# # PHC-TS06-TC033
# def test_agent_setting_long_intro(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["over_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     btn = agent_page.check_btn_disabled()
#     error = agent_page.error_message().text.strip()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC033 : Test Fail"
#     assert "한줄" or "Description" in error, "PHC-TS06-TC033 : Test Fail"
#     print("PHC-TS06-TC033 : Test Success")
    
# # PHC-TS06-TC034  
# def test_agent_setting_no_rule(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input("")
#     agent_page.setting_card_input(card)
#     btn = agent_page.check_btn_disabled()
#     error = agent_page.error_message().text.strip()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC034 : Test Fail"
#     assert "규칙" or "prompt" in error, "PHC-TS06-TC034 : Test Fail"
#     print("PHC-TS06-TC034 : Test Success")
    
# # PHC-TS06-TC035  
# def test_agent_setting_long_rule(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["over_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     time.sleep(3)
#     btn = agent_page.check_btn_disabled()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC035 : Test Fail"
#     print("PHC-TS06-TC035 : Test Success")

# # PHC-TS06-TC036  
# def test_agent_setting_delete_card(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_card_input(card)
#     elements = agent_page.check_card_number()
#     assert len(elements) == 2, "PHC-TS06-TC036 : Test Fail"
#     agent_page.delete_card()
#     elements = agent_page.check_card_number()
#     assert len(elements) == 1, "PHC-TS06-TC036 : Test Fail"
#     print("PHC-TS06-TC036 : Test Success")

# # PHC-TS06-TC037 
# def test_agent_setting_no_card(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input("")
#     time.sleep(2)
#     btn = agent_page.check_btn_disabled()
    
#     assert btn.get_attribute("disabled") is None, "PHC-TS06-TC037 : Test Fail"
#     print("PHC-TS06-TC037 : Test Success")
    
# # PHC-TS06-TC038 
# def test_agent_setting_long_card(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["over_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
#     time.sleep(2)
#     btn = agent_page.check_btn_disabled()
    
#     assert btn.get_attribute("disabled") is not None, "PHC-TS06-TC038 : Test Fail"
#     print("PHC-TS06-TC038 : Test Success")

# # PHC-TS06-TC039
# def test_agent_setting_many_option(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
    
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     intro = data["setting_inputs"][1]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     card = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_intro_input(intro)
#     agent_page.setting_rule_input(rule)
#     agent_page.setting_card_input(card)
    
#     agent_page.scroll_down_setting()
#     agent_page.multi_function()
#     time.sleep(2)
    
#     btn = agent_page.check_btn_disabled()
    
#     assert btn.get_attribute("disabled") is None, "PHC-TS06-TC039 : Test Fail"
#     print("PHC-TS06-TC039 : Test Success")

# # PHC-TS06-TC040
# def test_agent_image_upload(logged_in_agent):
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.upload_image("test_asset.jpg")

#     # 업로드 성공 여부 검증
#     uploaded = agent_page.check_upload_image()
#     assert uploaded.is_displayed(), "PHC-TS06-TC040 : Test Fail"
#     print("PHC-TS06-TC040 : Test Success")
    
# PHC-TS06-TC041
# def test_agent_big_image_upload(logged_in_agent):
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.upload_image("test_big_img.tif")
    
#     # 업로드 성공 여부 검증
#     assert agent_page.check_upload_big_img(), "PHC-TS06-TC041 : Test Fail"
#     print("PHC-TS06-TC041 : Test Success")

# PHC-TS06-TC042
# def test_agent_image_exe_upload(logged_in_agent,fm):
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_rule_input(rule)
#     time.sleep(2)
#     agent_page.upload_image("test_exe.exe")
#     error = agent_page.error_message()
    
#     # 업로드 성공 여부 검증
#     uploaded = agent_page.check_upload_image()
#     assert uploaded is None, "PHC-TS06-TC042 : Test Fail"
#     # 오류메시지 추가
#     assert error is not None, "PHC-TS06-TC042 : Test Fail"
#     print("PHC-TS06-TC042 : Test Success")
    
# PHC-TS06-TC043
# def test_agent_make_image(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_rule_input(rule)
#     time.sleep(2)
#     agent_page.make_image()
    
#     uploaded = agent_page.check_upload_image()
#     assert uploaded.is_displayed(), "PHC-TS06-TC043 : Test Fail"
#     print("PHC-TS06-TC043 : Test Success")

# PHC-TS06-TC044
# def test_agent_file_upload(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.scroll_down_setting()
    
#     # 파일 업로드
#     agent_page.upload_file("test_pdf.pdf")
#     uploaded = agent_page.check_upload_file()
#     assert uploaded, "PHC-TS06-TC044 : Test Fail"
#     print("PHC-TS06-TC044 : Test Success")
    
# PHC-TS06-TC045
# def test_agent_upload_img_to_file(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.scroll_down_setting()
    
#     # 파일 업로드
#     agent_page.upload_file("test_asset.jpg")
#     uploaded = agent_page.check_upload_file()
#     assert uploaded, "PHC-TS06-TC045 : Test Fail"
#     print("PHC-TS06-TC045 : Test Success")

# PHC-TS06-TC046
# def test_agent_upload_big_file(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.scroll_down_setting()
#     agent_page.upload_file("big_file.md")
#     uploaded = agent_page.check_fail_file_upload()
#     assert uploaded, "PHC-TS06-TC046 : Test Fail"
#     msg = agent_page.check_fail_msg_file_upload()
#     assert '크기' or 'size' in msg.text.strip(), "PHC-TS06-TC046 : Test Fail"
#     print("PHC-TS06-TC046 : Test Success")
    
# PHC-TS06-TC047
# def test_agent_upload_exe_to_file(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.scroll_down_setting()
#     agent_page.upload_file("test_exe.exe")
#     uploaded = agent_page.check_fail_file_upload()
#     assert uploaded, "PHC-TS06-TC047 : Test Fail"
#     msg = agent_page.check_fail_msg_file_upload()
#     assert msg is not None, "PHC-TS06-TC047 : Test Fail"
#     print("PHC-TS06-TC047 : Test Success")
    
# PHC-TS06-TC048
# def test_agent_upload_many_file(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_rule_input(rule)
#     time.sleep(2)
#     agent_page.scroll_down_setting()
#     agent_page.upload_multiple_images(limit=21)
#     error = agent_page.error_message().text.strip()
#     assert not "20개" or "" in error, "PHC-TS06-TC048 : Test Fail"
#     print("PHC-TS06-TC048 : Test Success")
    
# PHC-TS06-TC049
# def test_agent_delete_uploaded_file(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     agent_page.scroll_down_setting()
#     agent_page.upload_file("test_asset.jpg")
#     uploaded = agent_page.check_upload_file()
#     if uploaded :
#         agent_page.delete_for_uploaded_file()
#     uploaded = agent_page.check_upload_file()
#     assert uploaded is None, "PHC-TS06-TC049 : Test Fail"
#     print("PHC-TS06-TC049 : Test Success")
    
# PHC-TS06-TC051
# def test_agent_back_while_make(logged_in_agent) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.go_to_my_agent()
#     time.sleep(2)
#     agent_page.make_agent_screen()
#     time.sleep(2)
#     agent_page.back_in_agent_make_screen()
#     msg = agent_page.check_draft_msg().text.strip()
#     assert "초안" or "Draft" in msg, "PHC-TS06-TC051 : Test Fail"
#     print("PHC-TS06-TC051 : Test Success")

# # PHC-TS06-TC052
# def test_agent_refresh_preview(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     input = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_rule_input(rule)
#     time.sleep(2)
    
#     agent_page.preview_input_chat_stop(input)
#     text = agent_page.check_my_talk_input()
#     assert text is not None, "PHC-TS06-TC052 : Test Fail"
#     agent_page.refresh_btn_in_preview()
#     text = agent_page.check_my_talk_input()
#     assert text is None, "PHC-TS06-TC052 : Test Fail"
#     print("PHC-TS06-TC052 : Test Success")

# # PHC-TS06-TC055
# def test_agent_stop_chat_in_preview(logged_in_agent, fm) :
#     agent_page = logged_in_agent
#     agent_page.go_to_agent_page()
#     agent_page.make_agent_screen()
#     data = fm.read_json_file("agent_text_data.json")
#     name = data["setting_inputs"][0]["content"]
#     rule = data["setting_inputs"][2]["content"]
#     input = data["setting_inputs"][3]["content"]
#     agent_page.setting_name_input(name)
#     agent_page.setting_rule_input(rule)
#     time.sleep(2)
#     result = agent_page.preview_input_chat_stop(input)
#     assert result == AIresponse.STOPPED, "PHC-TS06-TC055 : Test Fail"
#     print("PHC-TS06-TC055 : Test Success")
    