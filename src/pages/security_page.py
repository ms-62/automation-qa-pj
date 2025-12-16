from utils.headers import *

from pages.base_page import BasePage
from utils.defines import TARGET_URL, NAME, XPATH


class SecurityPage(BasePage):
    #회원가입 페이지에서 보안 테스트 진행
    def go_to_signup_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
        time.sleep(1)
        create_button = self.get_element_by_xpath(XPATH["BTN_CREATE_ACCOUNT"])
        create_button.click()
        time.sleep(1)
        create_withemail = self.get_element_by_xpath(XPATH["BTN_CREATE_EMAIL"])
        create_withemail.click()
        time.sleep(1)
        print("회원 가입 페이지로 이동")
    
    def signup_email(self, data) :
        element = self.get_element_by_name(NAME["INPUT_ID"])
        element.click()
        element.clear()
        time.sleep(0.5)
        print("입력 완료")
        return element
    
    # def signup_name(self, name) :
    #     element = self.get_element_by_name(NAME["INPUT_NAME"])
    #     element.click()
    #     element.clear()
    #     element.send_keys(name)
    #     time.sleep(0.5)
    #     print("이름 입력 완료")
    #     return element
    
    #로그인
    
    
    #메인
    # def go_to_main_page(self):
    #     self.go_to_page(TARGET_URL["MAIN_URL"])
    #     time.sleep(4) 
        
    #계정 관리
    