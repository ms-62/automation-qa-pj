from utils.headers import *

from pages.base_page import BasePage
from utils.defines import NAME, XPATH,SELECTORS, TARGET_URL

class LoginPage(BasePage):
    def go_to_login_page(self):
        self.go_to_page(TARGET_URL["LOGIN_URL"])
        
    # 입력값 제어 메서드
    def input_id(self, username):
        element = self.get_element_by_name(NAME["INPUT_ID"])
        element.click()
        element.clear()
        element.send_keys(username)
        self.driver.implicitly_wait(0.3)

    def input_pw(self, password):
        element = self.get_element_by_name(NAME["INPUT_PW"])
        element.click()
        element.clear()
        element.send_keys(password)
        self.driver.implicitly_wait(0.3)

    def input_user_data(self, user_data):
        # user_data가 리스트인 경우 첫 번째 원소 사용
        if isinstance(user_data, list):
            user_data = user_data[0]
        self.input_id(user_data["username"])
        self.input_pw(user_data["password"])
        
    def clear_id(self):
        element = self.get_element_by_name(NAME["INPUT_ID"])
        element.click()
        element.clear()
        self.driver.implicitly_wait(0.1)

    def clear_pw(self):
        element = self.get_element_by_name(NAME["INPUT_PW"])
        element.click()
        element.clear()
        self.driver.implicitly_wait(0.1)

    def clear_all_inputs(self):
        self.clear_id()
        self.clear_pw()

    # 버튼 제어 메서드
    def click_login_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_LOGIN"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    # 로그인 실패/유효성 검증 메서드
    def is_error_msg_displayed(self):
        element = self.get_element_by_xpath(XPATH["TXT_LOGIN_ERROR"])
        return element is not None and element.is_displayed()
    
    def get_error_msg(self):
        element = self.get_element_by_xpath(XPATH["TXT_LOGIN_ERROR"])
        if element is None:
            return ""
        return element.text
    
    def is_id_invalid_msg_displayed(self):
        element = self.get_element_by_xpath(XPATH["TXT_LOGIN_INVALID"])
        return element is not None and element.is_displayed()
    
    def get_id_invalid_msg(self):
        element = self.get_element_by_xpath(XPATH["TXT_LOGIN_INVALID"])
        if element is None:
            return ""
        return element.text
    
    def is_pw_invalid_msg_displayed(self):
        element = self.get_element_by_xpath(XPATH["TXT_PW_INVALID"])
        return element is not None and element.is_displayed()
    
    def get_pw_invalid_msg(self):
        element = self.get_element_by_xpath(XPATH["TXT_PW_INVALID"])
        if element is None:
            return ""
        return element.text
    
    def is_login_page(self):
        try:
            self.get_element_by_xpath(XPATH["BTN_LOGIN"])
            return True
        except:
            return False

    def is_main_page(self):
        try:
            self.get_element_by_xpath(XPATH["AGENT_MENU_BTN"])
            return True
        except:
            return False
    
    def is_history_signin_page(self):
        url = self.driver.current_url
        return "/accounts/signin/history" in url
        
    # 로그아웃 기능 메서드
    def click_account_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_ACCOUNT"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def click_logout_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_LOGOUT"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def logout(self):
        self.click_account_button()
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, XPATH["BTN_LOGOUT"])
            )
        )
        self.click_logout_button()
        self.driver.implicitly_wait(0.3)
        
    def is_logged_out_page(self):
        return len(self.driver.find_elements(By.XPATH, XPATH["NICE_TO_MEET_YOU_AGIN_PAGE"])) > 0
    
    # View Password 기능 메서드
    def click_view_password_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_VIEW_PASSWORD"])
        btn.click()
        self.driver.implicitly_wait(0.3)
    
    def is_password_visible(self):
        pw_input = self.get_element_by_name(NAME["INPUT_PW"])
        if pw_input is None:
            return False
        return pw_input.get_attribute("type") == "text"
    
    def is_password_masked(self):
        pw_input = self.get_element_by_name(NAME["INPUT_PW"])
        if pw_input is None:
            return False
        return pw_input.get_attribute("type") == "password"
    
    # Forgot password 기능 메서드
    def click_forgot_password_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_FORGOT_PASSWORD"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def get_current_url(self): # 현재 URL 가져오기
        return self.driver.current_url  
    
    def is_forgot_password_page(self):
        url = self.driver.current_url
        return "recover" in url or "password" in url
        
    # Sign in with a different account 기능 메서드
    def click_diff_account_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_DIFF_ACCOUNT"])
        btn.click()
        self.driver.implicitly_wait(0.3)   
    
    # Remove history 기능 메서드
    def click_remove_history_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_REMOVE_HISTORY"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def get_id_value(self): # 
        element = self.get_element_by_name(NAME["INPUT_ID"])
        return element.get_attribute("value")

    def get_pw_value(self):
        element = self.get_element_by_name(NAME["INPUT_PW"])
        return element.get_attribute("value")
    
    def is_inputs_cleared(self):
        return self.get_id_value() == "" and self.get_pw_value() == ""