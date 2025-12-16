from utils.headers import *
from pages.login_page import (LoginPage)
from utils.browser_utils import (BrowserUtils)
from utils.defines import TARGET_URL

# PHC-TS01-TC001: Login 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.input_id("qa3team0202@elicer.com") 
    login_page.input_pw("team02fighting!") 
    login_page.click_login_button()
    assert login_page.is_main_page(), "로그인이 실행되지 않음"
    print("PHC-TS01-TC001 : Test success")
    
# PHC-TS01-TC002: 유효하지 않은 아이디 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.input_id("wrongtest@gmail.com") 
    login_page.input_pw("team02fighting!") 
    login_page.click_login_button()
    assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
    assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
    print("PHC-TS01-TC002 : Test success")

# PHC-TS01-TC003: 유효하지 않은 비밀번호 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.input_id("qa3team0202@elicer.com") 
    login_page.input_pw("validpass123!")
    login_page.click_login_button()
    assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
    assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
    print("PHC-TS01-TC003 : Test success")
    
# PHC-TS01-TC004: 유효하지 않은 아이디, 비밀번호 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.input_id("wrongtest@gmail.com")
    login_page.input_pw("validpass123!")
    login_page.click_login_button()
    assert login_page.is_error_msg_displayed(), "에러메시지 출력 안됨"
    assert login_page.get_error_msg() == "Email or password does not match", "에러메시지 오류"
    print("PHC-TS01-TC004 : Test success")
    
# PHC-TS01-TC005: 아이디 빈값 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.clear_id()
    login_page.input_pw("team02fighting!")
    login_page.click_login_button()
    assert login_page.is_id_invalid(), "아이디 입력값이 invalid 상태가 아님"
    print("PHC-TS01-TC005 : Test success")

# PHC-TS01-TC006: 비밀번호 빈값 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.input_id("qa3team0202@elicer.com")
    login_page.clear_pw()
    login_page.click_login_button()
    assert login_page.is_pw_invalid(), "비밀번호 입력값이 invalid 상태가 아님"
    print("PHC-TS01-TC006 : Test success")

# PHC-TS01-TC007: 아이디 빈값 테스트
def test_login(login_page):
    login_page.go_to_login_page()
    login_page.clear_all_inputs
    login_page.click_login_button()
    assert login_page.is_id_invalid(), "아이디 입력값이 invalid 상태가 아님"
    assert login_page.is_pw_invalid(), "아이디, 비밀번호 입력값이 invalid 상태가 아님"
    print("PHC-TS01-TC007 : Test success")

# PHC-TS01-TC008: Login 상태 유지 테스트
def test_keep_login(fm, user_data):
    # 첫 번째 브라우저 : 로그인 완료 후 종료
    dm1 = ChromeDriverManager()
    driver1 = dm1.create_driver()
    login_page1 = LoginPage(driver1)

    login_page1.go_to_login_page()
    login_page1.input_user_data(user_data)
    login_page1.click_login_button()
    
    bu = BrowserUtils()
    bu.save_cookies(driver1, fm)
    dm1.quit_driver()

    # 두 번째 브라우저: 재접속
    dm2 = ChromeDriverManager()
    driver2 = dm2.create_driver()
    login_page2 = LoginPage(driver2)

    bu.load_cookies(driver2, fm, TARGET_URL["MAIN_URL"])
    driver2.get(TARGET_URL["MAIN_URL"])

    assert not login_page2.is_history_signin_page(), "로그인 상태 유지 실패"
    dm2.quit_driver()
    print("PHC-TS01-TC008 : Test success")
    
# PHC-TS01-TC009: Logout 테스트
def test_logout(login_page):
    login_page.go_to_login_page()
    login_page.input_user_data() #테스트 데이터 입력
    login_page.click_login_button()
    login_page.click_account_button()
    login_page.click_logout_button()
    assert login_page.is_logged_out_page(), "로그아웃이 실행되지 않음"
    print("PHC-TS01-TC009 : Test success")

# PHC-TS01-TC010: View Password 테스트
def test_view_password(login_page):
    login_page.go_to_login_page()
    login_page.input_pw() # 테스트 데이터 입력
    assert login_page.is_password_masked(), "비밀번호 마스킹 실패"

    login_page.click_view_password_button()
    assert login_page.is_password_visible(), "비밀번호가 표시 상태(text)로 변경되지 않음"
    print("PHC-TS01-TC010 : Test success")
    
# PHC-TS01-TC011: Forgot password 테스트
def test_forgot_password(login_page):
    login_page.go_to_login_page()
    login_page.click_forgot_password_button()
    assert login_page.is_forgot_password_page(), "비밀번호 찾기 탭으로 이동 실패"
    print("PHC-TS01-TC011 : Test success")
    
# PHC-TS01-TC012: Sign up with different account 테스트
def test_diff_account(login_page):
    login_page.go_to_login_page()
    login_page.input_id() # 테스트 데이터 입력
    login_page.input_password() # 테스트 데이터 입력
    login_page.logout()
    login_page.click_diff_account_button()
    assert login_page.is_login_page(), "초기화되지 않음"
    print("PHC-TS01-TC012 : Test success")

# PHC-TS01-TC013: Remove History 테스트
def test_remove_history(login_page):
    login_page.go_to_login_page()
    login_page.input_id() # 테스트 데이터 입력
    login_page.input_password() # 테스트 데이터 입력
    login_page.logout()
    login_page.click_remove_history_button()
    assert login_page.is_inputs_cleared(), "Remove history 클릭 후 입력값이 초기화되지 않음"
    print("PHC-TS01-TC013 : Test success")