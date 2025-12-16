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
    
    def signup_email(self,data) :
        element = self.get_element_by_name(NAME["INPUT_ID"])
        element.click()
        element.clear()
        element.send_keys(data)
        time.sleep(0.5)
        print("이메일 sql 입력 완료")
        return element
    
    def signup_pw(self, data) :
        element = self.get_element_by_name(NAME["INPUT_PW"])
        element.click()
        element.clear()
        element.send_keys(data)
        time.sleep(0.5)
        print("비밀번호 sql 입력 완료")
        return element
    
    def signup_name(self, data) :
        element = self.get_element_by_name(NAME["INPUT_NAME"])
        element.click()
        element.clear()
        element.send_keys(data)
        time.sleep(0.5)
        print("이름 sql 입력 완료")
        return element

    def checkbox_spread(self) :
        header = self.get_element_by_id(ID["CHECKBOX_HEADER"])
        header.click()
        time.sleep(0.5)
        
    def signup_checkbox(self) :
        elements = self.get_elements_by_xpath(XPATH["SIGNUP_AGREE"])
        return elements
    
    def btn_create(self) :
        btn = self.get_element_by_xpath(XPATH["BTN_SIGNUP"])
        btn.click()
        success = self.get_element_by_xpath(XPATH["CHECK_SIGNUP"])
        input_email = self.get_element_by_name(NAME["INPUT_ID"], option="visibility", timeout=3)
        tooltip_msg = self.driver.execute_script("return arguments[0].validationMessage;", input_email)
        if tooltip_msg:
            print(tooltip_msg)
        else :
            print("sqli 발생")
            
        try:
            if "Forgot" in success:
                print("sqli 발생")
                return False
            else:
                print("sqli 대비 굿")
                return True
        except:    
            return True
    #로그인
    
    
    #메인
    # def go_to_main_page(self):
    #     self.go_to_page(TARGET_URL["MAIN_URL"])
    #     time.sleep(4) 
        
    #계정 관리
    