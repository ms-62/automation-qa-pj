from utils.headers import *
from pages.signup_page import (
    SignupPage
)
from utils.browser_utils import random_string

from test_logging.action_logger import log_action
from utils.context import TextContext, ActionResult
from utils.defines import TestResult

generated_email = None # 전역 변수, TC 1번째의 이메일을 받아 2번째 중복 테스트에 사용하려고

# PHC-TS02-TC001
def test_signup_success(signup_page, fm) :  
    # 로그인 성공 테스트
    test_name = "test_signup_success"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        global generated_email
        generated_email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{generated_email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        success = signup_page.check_signup_success()
        assert success is not None, "PHC-TS02-TC001 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_success"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS02-TC002
def test_signup_fail_duplicate(signup_page, fm) : 
    # 실패 테스트 - 중복 이메일
    test_name = "test_signup_fail_duplicate"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        global generated_email
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{generated_email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "already" in fail, "PHC-TS02-TC002 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_duplicate_email"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC003
def test_signup_fail_no_a(signup_page, fm) : 
    # 실패 테스트 - 이메일 주소에 @이 없음
    test_name = "test_signup_fail_no_a"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "incorrect" in fail, "PHC-TS02-TC003 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_no_a_in_email"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC004
def test_signup_fail_no_address(signup_page, fm) : 
    # 실패 테스트 - 이메일 @ 뒤 주소가 없음
    test_name = "test_signup_fail_no_address"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        email_input = signup_page.signup_email(f"{email}@")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        # 브라우저 기본 유효성 검사 툴팁
        msg = signup_page.driver.execute_script(
            "return arguments[0].validationMessage;", email_input
        )
        assert "@" in msg, "PHC-TS02-TC004 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_no_address_in_email"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise

# PHC-TS02-TC005
def test_signup_fail_notcomplete_address(signup_page, fm) : 
    # 실패 테스트 - 이메일 @ 뒤 주소가 완전하지 않음
    test_name = "test_signup_fail_notcomplete_address"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "incorrect" in fail, "PHC-TS02-TC005 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_incomplete_address_in_email")) 
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC006
def test_signup_fail_empty_email(signup_page, fm) : 
    # 실패 테스트 - 빈 이메일
    test_name = "test_signup_fail_empty_email"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        signup_page.go_to_signup_page()
        email_input = signup_page.signup_email("")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        # 브라우저 기본 유효성 검사 툴팁
        msg = signup_page.driver.execute_script(
            "return arguments[0].validationMessage;", email_input
        )
        assert "입력란" in msg, "PHC-TS02-TC006 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_empty_email")) 
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC007
def test_signup_fail_pw_less(signup_page, fm) : 
    # 실패 테스트 - 비밀번호 8자 미만
    test_name = "test_signup_fail_pw_less"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "password stronger!" in fail, "PHC-TS02-TC007 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_less_than_eight_pw")) 
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC008
def test_signup_success_pw_standard_length(signup_page, fm) :  
    # 성공 테스트 - 비밀번호 8자 기준값 테스트
    test_name = "test_signup_success_pw_standard_length"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf123!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        success = signup_page.check_signup_success()
        assert success is not None, "PHC-TS02-TC008 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_success_pw_standard_len"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC009
def test_signup_fail_pw_no_english(signup_page, fm) : 
    # 실패 테스트 -비밀번호에 영어 미포함
    test_name = "test_signup_fail_pw_no_english"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("12341234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "password stronger!" in fail, "PHC-TS02-TC009 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_no_english_in_pw"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC010
def test_signup_fail_pw_no_number(signup_page, fm) : 
    # 실패 테스트 -비밀번호에 숫자 미포함
    test_name = "test_signup_fail_pw_no_number"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdfasdf!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "password stronger!" in fail, "PHC-TS02-TC010 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_no_number_in_pw"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC011
def test_signup_fail_pw_no_character(signup_page, fm) : 
    # 실패 테스트 -비밀번호에 특수문자 미포함
    test_name = "test_signup_fail_pw_no_character"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdfg12345")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        fail = signup_page.check_signup_fail()
        assert "password stronger!" in fail, "PHC-TS02-TC011 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_no_character_in_pw"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC012
def test_signup_fail_empty_pw(signup_page, fm) : 
    # 실패 테스트 - 빈 비밀번호
    test_name = "test_signup_fail_empty_pw"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        password_input = signup_page.signup_pw("")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        # 브라우저 기본 유효성 검사 툴팁
        msg = signup_page.driver.execute_script(
            "return arguments[0].validationMessage;", password_input
        )
        assert "입력란" in msg, "PHC-TS02-TC012 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_empty_pw"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC013
def test_signup_fail_empty_name(signup_page, fm) : 
    # 실패 테스트 - 빈 이름
    test_name = "test_signup_fail_empty_name"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        name_input = signup_page.signup_name("")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.btn_create()
        # 브라우저 기본 유효성 검사 툴팁
        msg = signup_page.driver.execute_script(
            "return arguments[0].validationMessage;", name_input
        )
        assert "입력란" in msg, "PHC-TS02-TC013 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_empty_name"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC014
def test_signup_fail_no_agree(signup_page, fm) : 
    # 실패 테스트 - 개인정보 동의 미동의
    test_name = "test_signup_fail_no_agree"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        btn = signup_page.btn_element()
        assert btn.get_attribute("disabled") is not None, "PHC-TS02-TC014 : Test fail" 
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_with_no_agree"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC015
def test_signup_success_no_optional(signup_page, fm) : 
    # 성공 테스트 - 개인정보 동의 optional 항목 제외하고도 되는지
    test_name = "test_signup_success_no_optional"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.checkbox_spread()
        elements[4].click()
        signup_page.btn_create()
        success = signup_page.check_signup_success()
        assert success is not None, "PHC-TS02-TC015 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_success_with_no_optional_agree"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC016
def test_signup_fail_no_required(signup_page, fm) : 
    # 실패 테스트 - 개인정보 동의 required 항목 빼고 동의 시
    test_name = "test_signup_fail_no_required"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.checkbox_spread()
        elements[3].click()
        btn = signup_page.btn_element()
        assert btn.get_attribute("disabled") is not None, "PHC-TS02-TC016 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "signup_fail_with_no_required_agree"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
    
# PHC-TS02-TC017
def test_signup_14_age_verify(signup_page, fm) : 
    # 개인정보 동의 시 '14세 이상입니다' 항목 제외 시 테스트
    test_name = "test_signup_14_age_verify"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        elements = signup_page.signup_checkbox()
        elements[0].click()
        signup_page.checkbox_spread()
        elements[1].click()
        btn = signup_page.btn_element()
        if "Verify" in btn.text.strip() :
            btn.click()
            iframe = signup_page.iframe_element()
            signup_page.driver.switch_to.frame(iframe) # iframe 화면으로 이동
            pass_element = signup_page.iframe_pass_element()
            assert "통신사" in pass_element.text.strip(), "PHC-TS02-TC017 : Test fail"
            log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "verify_age_screen_when_signup_14_age"))
        else :
            try :
                signup_page.iframe_element()
            except TimeoutException as e:
                elapsed = time.perf_counter() - start
                fm.save_screenshot_png(signup_page.driver, test_name)
                log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
                raise
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise
            
# PHC-TS02-TC018
def test_signup_view_password(signup_page, fm) :
    # 비밀번호 보기 버튼 동작 확인
    test_name = "test_signup_view_password"
    ctx = TextContext(test_name, page="signup_page")
    start = time.perf_counter()
    try :
        email = random_string()
        signup_page.go_to_signup_page()
        signup_page.signup_email(f"{email}@gmail.com")
        element = signup_page.signup_pw("asdf1234!")
        signup_page.signup_name("이수진")
        signup_page.view_password()
        assert element.get_attribute("type") == "text", "PHC-TS02-TC018 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "view_password_option"))

        signup_page.view_password()
        assert element.get_attribute("type") == "password", "PHC-TS02-TC018 : Test fail"
        log_action(ctx, ActionResult(test_name, TestResult.PASSED, elapsed_time= 0, detail = "view_password_option_again"))
    except Exception as e:
        elapsed = time.perf_counter() - start
        fm.save_screenshot_png(signup_page.driver, test_name)
        log_action(ctx, ActionResult(test_name, TestResult.FAILED, elapsed, detail = str(e)))
        raise