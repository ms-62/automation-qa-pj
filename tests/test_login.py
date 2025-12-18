from utils.headers import *
from pages.login_page import (LoginPage)
from utils.browser_utils import (BrowserUtils)
from utils.browser_setup import create_driver
from utils.defines import TARGET_URL

# # PHC-TS01-TC001: Login 테스트
# def test_login(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com") 
#     login_page.input_pw("team02fighting!") 
#     login_page.click_login_button()
#     assert login_page.is_main_page(), "로그인이 실행되지 않음"
#     print("PHC-TS01-TC001 : Test success")
    
# # PHC-TS01-TC002: 유효하지 않은 아이디 테스트
# def test_invalid_id_login(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("wrongtest@gmail.com") 
#     login_page.input_pw("team02fighting!") 
#     login_page.click_login_button()
#     assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
#     print("PHC-TS01-TC002 : Test success")

# # PHC-TS01-TC003: 유효하지 않은 비밀번호 테스트
# def test_invalid_password_login(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com") 
#     login_page.input_pw("validpass123!")
#     login_page.click_login_button()
#     assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
#     print("PHC-TS01-TC003 : Test success")
    
# # PHC-TS01-TC004: 유효하지 않은 아이디, 비밀번호 테스트
# def test_invalid_id_password_login(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("wrongtest@gmail.com")
#     login_page.input_pw("validpass123!")
#     login_page.click_login_button()
#     assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
#     print("PHC-TS01-TC004 : Test success")
    
# # PHC-TS01-TC005: 아이디 빈값 테스트
# def test_null_id_login(login_page):
#     login_page.go_to_login_page()
#     login_page.clear_id()
#     login_page.input_pw("team02fighting!")
#     login_page.click_login_button()
#     assert login_page.is_login_page(), "아이디 입력값이 invalid 상태가 아님"
#     print("PHC-TS01-TC005 : Test success")

# # PHC-TS01-TC006: 비밀번호 빈값 테스트
# def test_null_password_login(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com")
#     login_page.clear_pw()
#     login_page.click_login_button()
#     assert login_page.is_login_page(), "비밀번호 입력값이 invalid 상태가 아님"
#     print("PHC-TS01-TC006 : Test success")

# # PHC-TS01-TC007: 아이디, 비밀번호 빈값 테스트
# def test_null_id_password_login(login_page):
#     login_page.go_to_login_page()
#     login_page.clear_all_inputs
#     login_page.click_login_button()
#     assert login_page.is_login_page(), "아이디, 비밀번호 입력값이 invalid 상태가 아님"
#     print("PHC-TS01-TC007 : Test success")

# # PHC-TS01-TC008: 아이디 @ 미포함
# def test_login_invalid_format(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202") 
#     login_page.input_pw("team02fighting!") 
#     login_page.click_login_button()
#     assert login_page.is_id_invalid_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_id_invalid_msg() == "Invalid email format.", "에러메시지 내용 오류"
#     print("PHC-TS01-TC008 : Test success")
    
# # PHC-TS01-TC009: 아이디가 이메일 주소를 따르지 않을 때
# def test_login_invalid_format2(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@") 
#     login_page.input_pw("team02fighting!") 
#     login_page.click_login_button()
#     assert login_page.is_id_invalid_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_id_invalid_msg() == "Invalid email format.", "에러메시지 내용 오류"
#     print("PHC-TS01-TC008 : Test success")
    
# # PHC-TS01-TC010: 비밀번호 8자리 이상 입력 확인
# def test_pw_invalid_format(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com") 
#     login_page.input_pw("team02") 
#     login_page.click_login_button()
#     assert login_page.is_pw_invalid_msg_displayed(), "에러메시지 출력 안됨"
#     assert login_page.get_pw_invalid_msg() == "Please enter a password of at least 8 digits.", "에러메시지 내용 오류"
#     print("PHC-TS01-TC009 : Test success")   

# # PHC-TS01-TC011: Login 상태 유지 테스트 -> 수동으로 돌려야 하나?
# def test_keep_login(fm, user_data, login_page):
#     # 첫 번째 브라우저 : 로그인 완료 후 종료
#     driver1 = create_driver("chrome")
#     login_page1 = LoginPage(driver1)

#     login_page1.go_to_login_page()
#     login_page1.input_user_data(user_data)
#     login_page1.click_login_button()
    
#     bu = BrowserUtils()
#     bu.save_cookies(driver1, fm, "login_cookies.json")
#     driver1.quit()

#     # 두 번째 브라우저: 재접속
#     driver2 = create_driver("chrome")
#     login_page2 = LoginPage(driver2)
    
#     driver2.get(TARGET_URL["MAIN_URL"])
#     bu.load_cookies(driver2, fm, TARGET_URL["MAIN_URL"], "login_cookies.json")
#     driver2.refresh()
    
#     assert not login_page2.is_login_page(), "로그인 상태 유지 실패"
#     driver2.quit()
#     print("PHC-TS01-TC011 : Test success")
        
# PHC-TS01-TC012: Logout 테스트
def test_logout(login_page_test):
    login_page_test.go_to_login_page()
    login_page_test.input_id("qa3team0202@elicer.com")
    login_page_test.input_pw("team02fighting!")
    login_page_test.click_login_button()
    login_page_test.click_account_button()
    login_page_test.click_logout_button()
    assert login_page_test.is_logged_out_page(), "로그아웃이 실행되지 않음"
    print("PHC-TS01-TC012 : Test success")

# PHC-TS01-TC013: View Password 테스트
def test_view_password(login_page_test):
    login_page_test.go_to_login_page()
    login_page_test.input_pw("team02fighting!") # 테스트 데이터 입력
    assert login_page_test.is_password_masked(), "비밀번호 마스킹 실패"

    login_page_test.click_view_password_button()
    assert login_page_test.is_password_visible(), "비밀번호가 표시 상태(text)로 변경되지 않음"
    print("PHC-TS01-TC013 : Test success")
    
# # PHC-TS01-TC014: Forgot password 테스트
# def test_forgot_password(login_page):
#     login_page.go_to_login_page()
#     login_page.click_forgot_password_button()
#     assert login_page.is_forgot_password_page(), "비밀번호 찾기 탭으로 이동 실패"
#     print("PHC-TS01-TC014 : Test success")
    
# # PHC-TS01-TC015: Sign up with different account 테스트
# def test_diff_account(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com")
#     login_page.input_pw("team02fighting!")
#     login_page.click_login_button()
#     login_page.logout()
#     login_page.click_diff_account_button()
#     assert login_page.is_login_page(), "초기화되지 않음"
#     print("PHC-TS01-TC015 : Test success")

# # PHC-TS01-TC016: Remove History 테스트
# def test_remove_history(login_page):
#     login_page.go_to_login_page()
#     login_page.input_id("qa3team0202@elicer.com") # 테스트 데이터 입력
#     login_page.input_pw("team02fighting!") # 테스트 데이터 입력
#     login_page.click_login_button()
#     login_page.logout()
#     login_page.click_remove_history_button()
#     assert login_page.is_inputs_cleared(), "Remove history 클릭 후 입력값이 초기화되지 않음"
#     print("PHC-TS01-TC016 : Test success")