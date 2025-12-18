from utils.headers import *

from pages.security_page import SecurityPage, SecurityMainPage

from utils.defines import TestResult
from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult

test_name = "test_input_security.py"
ctx = TextContext(test_name, page="security")
start = time.perf_counter()    

    
#로그인에서 sqli PHC-TS07-TC001
@pytest.mark.parametrize("case_key", ["sql_injection_a","sql_injection_b","sql_injection_c","sql_injection_d","sql_injection_e"])
def test_login_security_sql(security_signup_page,security_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_login_security_sql"))
    try:
        data = security_cases[case_key]
        security_signup_page.go_to_login_page()
        security_signup_page.input_id(data["sql_injection"]) 
        security_signup_page.input_pw(data["sql_injection"]) 
        assert not security_signup_page.click_login_button(), "로그인이 실행되지 않음"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "not security_signup_page.click_login_button"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
#회원가입에서 sqli PHC-TS07-TC002
@pytest.mark.parametrize("case_key", ["sql_injection_a","sql_injection_b","sql_injection_c","sql_injection_d","sql_injection_e"])
def test_signup_security_sql(security_signup_page,security_cases,case_key) :  
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_signup_security_sql"))    
    try:
        data = security_cases[case_key]
        security_signup_page.go_to_signup_page()
        security_signup_page.signup_email(data["sql_injection"])
        security_signup_page.signup_pw(data["sql_injection"])
        security_signup_page.signup_name(data["sql_injection"])
        
        elements = security_signup_page.signup_checkbox()
        elements[0].click()
        assert security_signup_page.btn_create(), "저장 진행, 에러발생 혹은 입력 불가"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.btn_create"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        
    
# #메인페이지 sqli PHC-TS07-TC003
def test_go_to(logged_in_main):
    page = logged_in_main

@pytest.mark.parametrize("case_key", ["sql_injection_a","sql_injection_b","sql_injection_c","sql_injection_d","sql_injection_e"])    
def test_main_security_sql(security_main_page,security_cases,case_key):    
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_main_security_sql"))    
    try:
        data = security_cases[case_key]
        assert security_main_page.input_chat(data["sql_injection"]), "검색 안됨 혹은 에러 발생"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.input_chat"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
#계정관리페이지 sqli PHC-TS07-TC004
def test_go_to_member(security_main_page):
        security_main_page.go_to_member_page()
        security_main_page.refresh_member_account_page()
        
@pytest.mark.parametrize("case_key", ["sql_injection_a","sql_injection_b","sql_injection_c","sql_injection_d","sql_injection_e"])
def test_member_security_sql(security_main_page, security_cases, case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_member_security_sql"))    
    try:  
        data = security_cases[case_key]
        security_main_page.open_name_edit_form()
        security_main_page.member_name(data["sql_injection"])
        assert security_main_page.submit_name() , "저장 진행, 에러발생 혹은 입력 불가"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.submit_name"))
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        

#xss
#로그인페이지 xss PHC-TS07-TC005
@pytest.mark.parametrize("case_key", ["xss_scipt_a","xss_scipt_b","xss_scipt_c"])
def test_login_security_xss(security_signup_page,security_cases,case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_login_security_xss"))    
    try:
        data = security_cases[case_key]
        security_signup_page.go_to_login_page()
        security_signup_page.input_id(data["xss_script"]) 
        security_signup_page.input_pw(data["xss_script"]) 
        assert not security_signup_page.click_login_button(), "로그인이 실행되지 않음" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "not security_signup_page.click_login_button"))    
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
        

#원가입에서 sqli PHC-TS07-TC006
@pytest.mark.parametrize("case_key", ["xss_scipt_a","xss_scipt_b","xss_scipt_c"])
def test_signup_security_xss(security_signup_page,security_cases,case_key) :  
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_signup_security_xss"))    
    try:
        data = security_cases[case_key]
        security_signup_page.go_to_signup_page()
        security_signup_page.signup_email(data["xss_script"])
        security_signup_page.signup_pw(data["xss_script"])
        security_signup_page.signup_name(data["xss_script"])
        elements = security_signup_page.signup_checkbox()
        elements[0].click()
        assert security_signup_page.btn_create(), "저장 진행, 에러발생 혹은 입력 불가"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.btn_create"))    
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
    
#메인페이지 sqli PHC-TS07-TC007
def test_go_to(logged_in_main):
    page = logged_in_main

@pytest.mark.parametrize("case_key", ["xss_scipt_a","xss_scipt_b","xss_scipt_c"])    
def test_main_security_xss(security_main_page,security_cases,case_key):    
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_main_security_xss"))    
    try:
        data = security_cases[case_key]
        assert security_main_page.input_chat(data["xss_script"]), "검색 안됨 혹은 에러 발생"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.input_chat"))    
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))
#계정관리페이지 sqli PHC-TS07-TC008
def test_go_to_member(security_main_page):
        security_main_page.go_to_member_page()
        security_main_page.refresh_member_account_page()
        
@pytest.mark.parametrize("case_key", ["xss_scipt_a","xss_scipt_b","xss_scipt_c"])
def test_member_security_xss(security_main_page, security_cases, case_key):
    log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "test_member_security_xss"))    
    try:
        data = security_cases[case_key]
        security_main_page.open_name_edit_form()
        security_main_page.member_name(data["xss_script"])
        assert security_main_page.submit_name() , "저장 진행, 에러발생 혹은 입력 불가"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "security_signup_page.submit_name"))  
    except:
        elapsed = time.perf_counter() - start
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed))