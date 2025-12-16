from utils.headers import *

from utils.context import LoginContext
from utils.defines import NAME, XPATH

class BrowserUtils:
    
    def save_cookies(self, driver, fm, file_name = "cookies.json"):
        cookies = driver.get_cookies()
        fm.save_json_file(file_name, cookies)

    def load_cookies(self, driver, fm, url, file_name = "cookies.json"):
        cookies = fm.read_json_file(file_name)
        if not cookies:
            print(f"쿠키 파일 없음")
            return False

        # 여기 부분 driver manager로 뺄수도.
        driver.get(url)
        time.sleep(0.5)
        for cookie in cookies:
            cookie.pop("domain", None)
            driver.add_cookie(cookie)
                
        return True

    #    loaded_cookies = self.load_cookies(ctx.driver, ctx.fm, ctx.url)
    
    def auto_login(self, ctx: LoginContext):
        ctx.main_page.go_to_main_page()

        # 로그인 여부를 dom 기반으로 확인
        el_id = ctx.login_page.get_element_by_name(NAME["INPUT_ID"], option = "visibility")
        el_pw = ctx.login_page.get_element_by_name(NAME["INPUT_PW"], option = "visibility")
        
        if el_id and el_pw:
            user = ctx.user_data[-1]
            ctx.login_page.input_user_data(user)
            ctx.login_page.click_login_button()
            self.save_cookies(ctx.driver, ctx.fm, ctx.file_name)
        elif el_pw and not el_id:
            user = ctx.user_data[-1]
            ctx.login_page.input_pw(user["password"])
            ctx.login_page.click_login_button()
            self.save_cookies(ctx.driver, ctx.fm, ctx.file_name)
        # 이미 있다
        else:
            print("로그인 폼이 없으니까 로그인 스킵")
        return ctx.main_page
    
    # 수진 - 추가
    def is_logged_in(self, driver):
        try:
            driver.find_element(By.XPATH, XPATH["AGENT_MENU_BTN"])
            return True
        except:
            return False

        
# 수진 - 회원가입 시 랜덤 이메일 주소 생성
def random_string(length=8):
    """영문 대소문자 + 숫자 조합으로 랜덤 문자열 생성"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))