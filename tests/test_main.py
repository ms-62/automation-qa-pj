from utils.headers import *

from pages.model_setting_page import ModelSettingPage
from pages.past_chats_page import PastChatsPage

from utils.defines import DEFAULT_MODEL, DEFAULT_CHAT

# main 홈화면 테스트만 진행합니다. 

# def test_conversation_text(logged_in_main, fm):
#     page = logged_in_main
#     page.click_btn_home_menu(DEFAULT_CHAT)
    
#     ai_input_lst = fm.read_json_file("ai_text_data.json")["inputs"]   
#     for item in ai_input_lst:
#         if item["type"] != "text":
#             continue   
#         page.input_chat(item["content"])  
        
#     page.click_btn_retry()
#     page.copy_last_response()
#     page.paste_last_response()
#     page.reset_chat()
    
#     page.scroll_up_chat()
#     page.scroll_down_chat()
#     page.click_btn_scroll_to_bottom()

    # 사용자가 보낸 메시지 내용 편집
    # 사용자가 보낸 메시지 내용 편집 중 취소
    # 사용자가 보낸 메시지 복사  
    
# def test_past_chats(logged_in_main):
#     page = logged_in_main
    
#     past_chat_page = PastChatsPage(driver)
  
    # 이름변경' 버튼 동작
    # 이름 변경 '취소' 버튼 동작
    # 삭제' 버튼 동작


# 파일 업로드 
def test_file_upload(logged_in_main, fm):
    page = logged_in_main

    images = fm.get_asset_files((".jpg", ".png"))
    for img in images:
        page.upload_file(os.path.basename(img))
    
    pdfs = fm.get_asset_files(".pdf")
    for pdf in pdfs:
        page.upload_file(os.path.basename(pdf))

    not_allowed_files = fm.get_asset_files(".psd")
    for file in not_allowed_files:
        page.upload_file(os.path.basename(file))






   

# def test_menu_scenario(logged_in_main):
#     page = logged_in_main
#     page.sync_menu_status()
#     page.action_menu_arrow()
#     page.action_menu_bar()
#     page.action_menu_bar()
#     page.action_menu_arrow()

# def test_model_setting(driver):
#     page = logged_in_main
#     model_page = ModelSettingPage(driver)
#     model_page.open_model_menu()
#     model_page.select_last_model()
#     model_page.open_model_menu()
#     model_page.go_to_model_setting()
#     model_page.toggle_all_models_and_verify()               
#     model_page.go_back() # 설정창 닫기
#     model_page.compare_active_models()  # 드롭다운 검증
    
