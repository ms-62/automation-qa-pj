from utils.headers import *

from utils.context import LoginContext
from utils.defines import NAME, XPATH

class BrowserUtils:
    
    def save_cookies(self, driver, fm, file_name):
        cookies = driver.get_cookies()
        data = {
            "timestamp": time.time(),
            "cookies": cookies
        }
        fm.save_json_file(file_name, data)

    def load_cookies(self, driver, fm, url, file_name):
        data = fm.read_json_file(file_name)
        if not data or "cookies" not in data:
            return False

        driver.get(url)
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        for cookie in data["cookies"]:
            cookie_copy = cookie.copy()
            cookie_copy.pop("sameSite", None)
            cookie_copy.pop("domain", None)  # 도메인 제거
            if "expiry" in cookie_copy:
                cookie_copy["expiry"] = int(cookie_copy["expiry"])
            try:
                driver.add_cookie(cookie_copy)
            except Exception as e:
                print(f"쿠키 추가 실패: {cookie_copy.get('name')} -> {e}")

        driver.refresh()
        return True
    
    def auto_login(self, ctx: LoginContext):
        ctx.main_page.go_to_main_page()
        if self.is_logged_in(ctx.driver):
            return ctx.main_page
        
        # loaded = self.load_cookies(ctx.driver, ctx.fm, ctx.url, ctx.file_name)
        # if loaded:
        #     ctx.main_page.go_to_main_page()
        #     if self.is_logged_in(ctx.driver):
        #         return ctx.main_page

        el_id = ctx.login_page.get_element_by_name(NAME["INPUT_ID"], option="visibility")
        el_pw = ctx.login_page.get_element_by_name(NAME["INPUT_PW"], option="visibility")
        user = ctx.user_data[-1]
        if el_id and el_pw:
            ctx.login_page.input_user_data(user)
        elif el_pw and not el_id:
            ctx.login_page.input_pw(user["password"])
        else:
            print("로그인 폼이 없으니까 로그인 스킵")
        ctx.login_page.click_login_button()

        if not self.is_logged_in(ctx.driver):
            raise Exception("auto_login 실패: 로그인 성공 확인 불가")
        self.save_cookies(ctx.driver, ctx.fm, ctx.file_name)
        return ctx.main_page
    
    # 수진 - 추가
    def is_logged_in(self, driver):
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, XPATH["AGENT_MENU_BTN"])
                )
            )
            return True
        except TimeoutException:
            return False

        
# 수진 - 회원가입 시 랜덤 이메일 주소 생성
def random_string(length=8):
    """영문 대소문자 + 숫자 조합으로 랜덤 문자열 생성"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))