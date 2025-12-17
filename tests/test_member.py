from utils.headers import *

from pages.member_page import MemberPage
#메인페이지 접속
def test_go_to_main(logged_in_main):
    page = logged_in_main
#계정관리 접속(새창)
def test_go_to_member(member_page): 
    member_page.go_to_member_page()
    
#PHC-TS05-TC001
def test_update_name_normal(member_page,test_cases):
    data = test_cases["normal"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(), "저장 버튼 클릭 또는 저장 실패"

def test_update_name_tab_blank(member_page,test_cases):
    data = test_cases["spacebar_blank"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert not member_page.submit_name(), "해당 내용 저장 성공"

def test_update_name_spacebar_blank(member_page,test_cases):
    data = test_cases["tab_blank"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert not member_page.submit_name(), "해당 내용 저장 성공"

def test_update_name_newline(member_page,test_cases):
    data = test_cases["newline"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert not member_page.submit_name(), "해당 내용 저장 성공"

def test_update_name_code_html(member_page,test_cases):
    data = test_cases["code_html"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(), "저장 버튼 클릭 또는 저장 실패"

def test_update_name_character_blank(member_page,test_cases):
    data = test_cases["character_blank"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(), "저장 버튼 클릭 또는 저장 실패"
    
# # #PHC-TS05-TC002
def test_update_name_maximum(member_page,test_cases):
    data = test_cases["maximum_name"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(),  "저장 버튼 클릭 또는 저장 실패"

#PHC-TS05-TC003
def test_update_name_lang_thai_true(member_page,test_cases):
    data = test_cases["thai_name_t"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(),  "저장 버튼 클릭 또는 저장 실패"

def test_update_name_lang_thai_false(member_page,test_cases):
    data = test_cases["thai_name_f"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    saved = member_page.submit_name()
    assert saved is False, "타언어 입력인데도 저장이 성공함 (오류가 나지 않음)"

def test_update_name_lang_jpn_true(member_page,test_cases):
    data = test_cases["jpn_name_t"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(),  "저장 버튼 클릭 또는 저장 실패"

def test_update_name_lang_jpn_false(member_page,test_cases):
    data = test_cases["jpn_name_f"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    saved = member_page.submit_name()
    assert saved is False, "타언어 입력인데도 저장이 성공함 (오류가 나지 않음)"

def test_update_name_lang_eng_true(member_page,test_cases):
    data = test_cases["eng_name_t"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    assert member_page.submit_name(),  "저장 버튼 클릭 또는 저장 실패"

def test_update_name_lang_eng_false(member_page,test_cases):
    data = test_cases["eng_name_f"]
    assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
    assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
    assert member_page.member_name(data["value"]), "이름 입력 실패"
    saved = member_page.submit_name()
    assert saved is False, "타언어 입력인데도 저장이 성공함 (오류가 나지 않음)"

#PHC-TS05-TC004
def test_update_email_blank(member_page,test_cases):
    data = test_cases["email_blank_tab"] 
    assert member_page.refresh_member_account_page()
    assert member_page.open_email_edit_form()
    assert member_page.member_email(data["value"])
    saved = member_page.certification_email()
    assert saved is False, "이메일 주소 형식 틀림으로 저장 불가" 

def test_update_email_duplication(member_page,test_cases):
    data = test_cases["email_duplication"]
    assert member_page.refresh_member_account_page()
    assert member_page.open_email_edit_form()
    assert member_page.member_email(data["value"])
    saved = member_page.certification_email()
    assert saved is False, "이메일 주소 형식 틀림으로 저장 불가" 

def test_update_email_character(member_page,test_cases):
    data = test_cases["email_character"]
    assert member_page.refresh_member_account_page()
    assert member_page.open_email_edit_form()
    assert member_page.member_email(data["value"])
    saved = member_page.certification_email()
    assert saved is False, "이메일 주소 형식 틀림으로 저장 불가" 

# #PHC-TS05-TC006
def test_update_mobile(member_page,test_cases):
    data = test_cases["mobile"]
    assert member_page.refresh_member_account_page()
    assert member_page.open_mobile_edit_form()
    assert member_page.member_mobile(data["value"])
    assert member_page.certification_mobile()

# #PHC-TS05-TC008
def test_update_fail_pwd(member_page,test_cases):
    data = test_cases["valid_pwd"]
    assert member_page.refresh_member_account_page()
    assert member_page.open_pwd_edit_form()
    assert member_page.member_fail_pwd(data["value"])
    saved = member_page.change_fail_pwd()
    assert saved is False, "비밀번호 변경 성공, (실패해야함)" 

#PHC-TS05-TC009 비밀번호 변경이라 이후 작업을 위해 블락
# def test_update_fail_pwd(member_page,test_cases):
#     data = test_cases["exist_pwd"]
#     data_new = test_cases["valid_pwd"]
#     assert member_page.refresh_member_account_page()
#     assert member_page.open_pwd_edit_form()
#     assert member_page.member_success_pwd(data["value"],data_new["value"])
#     assert member_page.change_success_pwd()

#PHC-TS05-TC010
def test_update_lang(member_page):
    assert member_page.open_lang_edit_form()
    assert member_page.choose_lang_dropbox()
    assert member_page.refresh_member_account_page()
    assert member_page.choose_lang_check()
    member_page.revoke_lang_kor() #다음 테스트를 위한 언어 원복 메서드 필요, 테스트 항목 아님

#PHC-TS05-TC011 DOM 아닌 영역 새로고침 메서드 제외하고 진행
def test_oauth_google(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_google_click()
    assert member_page.oauth_popup_open_close()    

#PHC-TS05-TC012
def test_oauth_naver(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_naver_click()
    assert member_page.oauth_popup_open_close()
    
#PHC-TS05-TC013 DOM 아닌 영역 새로고침 메서드 제외하고 진행
def test_oauth_kko(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_kko_click()
    assert member_page.oauth_popup_open_close()

#PHC-TS05-TC014
def test_oauth_github(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_github_click()
    assert member_page.oauth_popup_open_close()

#PHC-TS05-TC015
def test_oauth_whalespace(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_whalespace_click()
    assert member_page.oauth_popup_open_close()

#PHC-TS05-TC016
def test_oauth_apple(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_apple_click()
    assert member_page.oauth_popup_open_close()

#PHC-TS05-TC017
def test_oauth_facebook(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_facebook_click()
    assert member_page.oauth_popup_open_close()

#PHC-TS05-TC018
def test_oauth_microsoft(member_page):
    assert member_page.open_oauth_edit_form()
    assert member_page.oauth_microsoft_click()
    assert member_page.oauth_popup_open_close()        
    
# #PHC-TS05-TC019 해당 관련 항목 자동화로 비교하려고 했는데 시간 부족하면 수동으로 변경 
# def test_toast_save_info(member_page,test_cases):
#     data = test_cases["normal"]
#     assert member_page.open_name_edit_form()
#     assert member_page.member_name(data["value"])
#     assert member_page.submit_name()
#     assert member_page.click_to_promotion()
#     assert member_page.toast_save_msg_compare()
#     member_page.save_report_data()