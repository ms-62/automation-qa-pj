from utils.headers import *

from pages.base_page import BasePage
from utils.defines import TARGET_URL, XPATH, ID, NAME
import logging

logger = logging.getLogger()
class SignupPage(BasePage):
    def go_to_signup_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
        self.get_element_by_xpath(XPATH["BTN_CREATE_ACCOUNT"], option="clickable").click()
        self.get_element_by_xpath(XPATH["BTN_CREATE_EMAIL"], option="clickable").click()
        logger.info("회원 가입 페이지로 이동")
        
    def signup_email(self, email) :
        element = self.get_element_by_name(NAME["INPUT_ID"], option="clickable")
        element.click()
        element.clear()
        element.send_keys(email)
        logger.info("이메일 입력 완료")
        return element
        
    def signup_pw(self, password) :
        element = self.get_element_by_name(NAME["INPUT_PW"], option="clickable")
        element.click()
        element.clear()
        element.send_keys(password)
        logger.info("비밀번호 입력 완료")
        return element
        
    def signup_name(self, name) :
        element = self.get_element_by_name(NAME["INPUT_NAME"], option="clickable")
        element.click()
        element.clear()
        element.send_keys(name)
        logger.info("이름 입력 완료")
        return element
        
    def checkbox_spread(self) :
        header = self.get_element_by_id(ID["CHECKBOX_HEADER"], option="clickable")
        header.click()
        
    def signup_checkbox(self) :
        elements = self.get_elements_by_xpath(XPATH["SIGNUP_AGREE"])
        return elements
    
    def btn_create(self) :
        btn = self.get_element_by_xpath(XPATH["BTN_SIGNUP"], option="clickable")
        btn.click()
        
    def btn_element(self) :
        btn = self.get_element_by_xpath(XPATH["BTN_SIGNUP"])
        return btn
        
    def check_signup_success(self) :
        success = self.get_element_by_xpath(XPATH["CHECK_SIGNUP"])
        logger.info("회원가입 완료")
        return success
    
    def check_signup_fail(self) :
        fail = self.get_element_by_xpath(XPATH["SIGNUP_FAIL"], option="visibility")
        return fail.text.strip()
    
    def iframe_element(self) :
        iframe = self.get_element_by_xpath(XPATH["PASS_IFRAME"])
        logger.info("본인인증 화면 로드 완료")
        return iframe
    
    def iframe_pass_element(self) :
        element = self.get_element_by_xpath(XPATH["PASS_ELEMENT"])
        return element
    
    def view_password(self) :
        element = self.get_element_by_xpath(XPATH["SIGNUP_VIEW_PW"])
        element.click()
    