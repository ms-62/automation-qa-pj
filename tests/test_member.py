from utils.headers import *
from pages.member_page import MemberPage

import logging
from utils.defines import TestResult
from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult

logger = logging.getLogger()

#메인페이지 접속

def test_go_to_main(logged_in_main):
    page = logged_in_main
#계정관리 접속(새창)
def test_go_to_member(member_page): 
    member_page.go_to_member_page()

test_name = "test_member.py"
ctx = TextContext(test_name, page="member")
start = time.perf_counter()    

#PHC-TS05-TC001
@pytest.mark.parametrize("case_key", ["normal"])
def test_update_name_normal(member_page,test_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_name_normal"))
    try:
        data = test_cases[case_key]
        assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_name_edit_form"))
        assert member_page.member_name(data["value"]), "이름 입력 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_name"))
        
        assert member_page.submit_name(), "저장 버튼 클릭 또는 저장 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
@pytest.mark.parametrize("case_key", ["tab_blank","spacebar_blank","newline","code_html","character_blank"])
def test_update_name_not_save(member_page,test_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_name_not_save"))
    try:
        data = test_cases[case_key]
        assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_name_edit_form"))
        assert member_page.member_name(data["value"]), "이름 입력 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_name"))
        
        assert not member_page.submit_name(), "해당 내용 저장 성공"
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed_time= 0, detail = "submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
#PHC-TS05-TC002
def test_update_name_maximum(member_page,test_cases):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_name_maximum"))
    try:
        data = test_cases["maximum_name"]
        assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_name_edit_form"))
        assert member_page.member_name(data["value"]), "이름 입력 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_name"))
        
        assert not member_page.submit_name(),  "해당 내용 저장 성공"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
#PHC-TS05-TC003
@pytest.mark.parametrize("case_key", ["thai_name_t","jpn_name_t","eng_name_t"])
def test_update_name_lang_true(member_page,test_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_name_lang_true"))
    try:
        data = test_cases[case_key]
        assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_name_edit_form"))
        assert member_page.member_name(data["value"]), "이름 입력 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_name"))
        
        assert member_page.submit_name(),  "저장 버튼 클릭 또는 저장 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
@pytest.mark.parametrize("case_key", ["thai_name_f","jpn_name_f","eng_name_f"])
def test_update_name_lang_false(member_page,test_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_name_lang_false"))
    
    try:
        data = test_cases[case_key]
        assert member_page.refresh_member_account_page() , "계정관리 페이지 새로고침 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_name_edit_form() , "이름 수정 폼 열기 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_name_edit_form"))
        assert member_page.member_name(data["value"]), "이름 입력 실패"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_name"))
        saved = member_page.submit_name()
        
        assert saved is False, "타언어 입력인데도 저장이 성공함 (오류가 나지 않음)"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC004
@pytest.mark.parametrize("case_key", ["email_blank_tab","email_duplication","email_character"])
def test_update_email_not_save(member_page,test_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_email_not_save"))
    try:
        data = test_cases[case_key] 
        assert member_page.refresh_member_account_page()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_email_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_email_edit_form"))
        assert member_page.member_email(data["value"])
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_email"))
        saved = member_page.certification_email()
        
        assert saved is False, "이메일 주소 형식 틀림으로 저장 불가" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "certification_email"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

# #PHC-TS05-TC006
def test_update_mobile(member_page,test_cases):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_mobile"))
    try:
        data = test_cases["mobile"]
        assert member_page.refresh_member_account_page()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_mobile_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_mobile_edit_form"))
        assert member_page.member_mobile(data["value"])
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_mobile"))
        assert member_page.certification_mobile()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "certification_mobile"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

# #PHC-TS05-TC008
def test_update_fail_pwd(member_page,test_cases):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_fail_pwd"))
    try:
        data = test_cases["valid_pwd"]
        assert member_page.refresh_member_account_page()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.open_pwd_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_pwd_edit_form"))
        assert member_page.member_fail_pwd(data["value"])
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_fail_pwd"))
        saved = member_page.change_fail_pwd()
        
        assert saved is False, "비밀번호 변경 성공, (실패해야함)" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "change_fail_pwd"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC009 비밀번호 변경이라 이후 작업을 위해 블락
# def test_update_pass_pwd(member_page,test_cases):
#     log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_pass_pwd"))
#     try:
#         data = test_cases["exist_pwd"]
#         data_new = test_cases["valid_pwd"]
#         assert member_page.refresh_member_account_page()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
#         assert member_page.open_pwd_edit_form()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_pwd_edit_form"))
#         assert member_page.member_success_pwd(data["value"],data_new["value"])
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "member_success_pwd"))
#         assert member_page.change_success_pwd()
#         log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "change_success_pwd"))
#     except:
#         elapsed = time.perf_counter() - start
#         log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC010
def test_update_lang(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_update_lang"))
    try:
        assert member_page.open_lang_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_pwd_edit_form"))
        assert member_page.choose_lang_dropbox()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "choose_lang_dropbox"))
        assert member_page.refresh_member_account_page()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "refresh_member_account_page"))
        assert member_page.choose_lang_check()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "choose_lang_check"))
        member_page.revoke_lang_kor() #다음 테스트를 위한 언어 원복 메서드 필요, 테스트 항목 아님
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC011 DOM 아닌 영역 새로고침 메서드 제외하고 진행
def test_oauth_google(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_google"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_google_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_google_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC012
def test_oauth_naver(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_naver"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_naver_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_naver_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
#PHC-TS05-TC013
def test_oauth_kko(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_kko"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_kko_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_kko_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC014
def test_oauth_github(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_github"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_github_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_github_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC015
def test_oauth_whalespace(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_whalespace"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_whalespace_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_whalespace_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC016
def test_oauth_apple(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_apple"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_apple_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_apple_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC017
def test_oauth_facebook(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_facebook"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_facebook_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_facebook_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))

#PHC-TS05-TC018
def test_oauth_microsoft(member_page):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_oauth_microsoft"))
    try:
        assert member_page.open_oauth_edit_form()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "open_oauth_edit_form"))
        assert member_page.oauth_microsoft_click()
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_microsoft_click"))
        assert member_page.oauth_popup_open_close()    
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "oauth_popup_open_close"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))     
    
# #PHC-TS05-TC019 해당 관련 항목 자동화로 비교하려고 했는데 시간 부족하면 수동으로 변경 
# def test_toast_save_info(member_page,test_cases):
#     data = test_cases["normal"]
#     assert member_page.open_name_edit_form()
#     assert member_page.member_name(data["value"])
#     assert member_page.submit_name()
#     assert member_page.click_to_promotion()
#     assert member_page.toast_save_msg_compare()
#     member_page.save_report_data()