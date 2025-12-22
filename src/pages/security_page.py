from utils.headers import *

from pages.base_page import BasePage
from utils.defines import TARGET_URL, NAME, XPATH, SELECTORS,ID

from controllers.chat_input_controller import ChatInputController
import logging

logger = logging.getLogger()


class SecurityPage(BasePage):
    #로그인 페이지에서 보안 테스트 진행
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
        
        input_email = self.wait_for_element(
            By.NAME,
            NAME["INPUT_ID"],
            condition="clickable",
            timeout=3)
        tooltip_msg = self.driver.execute_script("return arguments[0].validationMessage;", input_email)
        if tooltip_msg:
            logger.info(tooltip_msg)
        else :
            logger.error("sqli 발생")
    
    #회원가입 페이지에서 보안 테스트 진행
    def go_to_signup_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
        self.driver.implicitly_wait(5)
        create_button = self.get_element_by_xpath(XPATH["BTN_CREATE_ACCOUNT"])
        create_button.click()
        self.driver.implicitly_wait(5)
        create_withemail = self.get_element_by_xpath(XPATH["BTN_CREATE_EMAIL"])
        create_withemail.click()
        self.driver.implicitly_wait(5)
        logger.info("회원 가입 페이지로 이동")
    
    def signup_email(self,data) :
        element = self.get_element_by_name(NAME["INPUT_ID"])
        element.click()
        element.clear()
        element.send_keys(data)
        logger.info("이메일 sql or xss 입력 완료")
        return element
    
    def signup_pw(self, data) :
        element = self.get_element_by_name(NAME["INPUT_PW"])
        element.click()
        element.clear()
        element.send_keys(data)
        logger.info("비밀번호 sql or xss 입력 완료")
        return element
    
    def signup_name(self, data) :
        element = self.get_element_by_name(NAME["INPUT_NAME"])
        element.click()
        element.clear()
        element.send_keys(data)
        logger.info("이름 sql or xss 입력 완료")
        return element

    def checkbox_spread(self) :
        header = self.get_element_by_id(ID["CHECKBOX_HEADER"])
        header.click()
        
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
            logger.info(tooltip_msg)
        else :
            logger.error("sqli 발생")
            
        try:
            if "Forgot" in success:
                logger.error("sqli 발생")
                return False
            else:
                logger.info("sqli 대비 굿")
                return True
        except:    
            return True

WAIT_TIME = 5    
class SecurityMainPage(BasePage):
    # ================= main 공용 ===================== #
    def click_btn_by_xpath(self, xpath, option, timeout=WAIT_TIME):
        btn = self.get_element_by_xpath(xpath, option)
        if not btn:
            return False
        try:
            WebDriverWait(self.driver, timeout).until(lambda d: btn.is_enabled())
            btn.click()
            return True
        except:
            return False
    
    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
        
    def input_chat(self, text):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
        return textarea
    
    def click_send(self):
        self.click_btn_by_xpath(XPATH["BTN_SEND"], option = "presence")
        
    #계정 관리
    def go_to_member_page(self):
        modal_btn = self.wait_for_element(
            By.CSS_SELECTOR,
            SELECTORS["MEMBER_MODAL"],
            condition="clickable",
            timeout=10)
        self.driver.execute_script("arguments[0].click();", modal_btn) #모달 무조건 스크립트로 클릭

        member_btn = self.wait_for_element(
            By.XPATH,
            XPATH["BTN_MEMBER"],
            condition="clickable",
            timeout=10)
        self.driver.execute_script("arguments[0].click();", member_btn)

        
        self.ensure_account_window()
        return True
    
    def refresh_member_account_page(self) -> bool:
        if "accounts.elice.io/members/account" not in self.driver.current_url:
            if not self.go_to_member_page():
                return False
        self.driver.refresh()
        return True

    #이름 관련 테스트 케이스를 위한 메서드
    def open_name_edit_form(self, timeout=5) -> bool:
        logger.info("open_name_edit_form 시작")

        # 0) '이름' 행 스크롤 위치 맞추기
        name_row = self.wait_for_element(
            By.XPATH, XPATH["NAME_ROW"], 
            condition="visibility", timeout=timeout
        )
        if not name_row:
            logger.error(" '이름' 행을 찾지 못함 (NAME_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, name_row)
        self.driver.implicitly_wait(0.3)

        # 1) '이름' 수정 버튼 찾기
        edit_btn = self.wait_for_element(
            By.XPATH, XPATH["BTN_NAME_EDIT"], 
            condition="clickable", timeout=timeout
        )
        if not edit_btn:
            logger.error("'이름' 수정 버튼 못 찾음 (BTN_NAME_EDIT)")
            return False

        logger.info("'이름' 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭 
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        
        self.driver.execute_script("arguments[0].click();", edit_btn)

        # 2) 이름 입력 필드 대기
        input_name = self.wait_for_element(
        By.NAME, NAME["INPUT_NAME"], 
        condition="clickable", timeout=timeout
    )
        if not input_name:
            logger.error("이름 입력란 안 나타남 (폼 안 열림)")
            return False

        logger.info("이름 수정 폼 열림")
        return True


    def member_name(self, name,timeout=5) -> bool:
        input_name = self.wait_for_element(
        By.NAME, NAME["INPUT_NAME"], 
        condition="clickable", timeout=timeout
    )
        if not input_name:
            logger.error("이름 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_name)
        self.driver.implicitly_wait(0.3)

        try:
            input_name.click()
        except Exception as e:
            logger.error(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_name)

        self.driver.execute_script("arguments[0].value = '';", input_name)
        input_name.send_keys(name)

        self.driver.implicitly_wait(0.5)
        logger.info(f"테스트 내용 입력 완료: {repr(name)}")
        return True


    def submit_name(self) -> bool:
        """저장 버튼 JS 클릭 + '이름' 행으로 스크롤 복귀 + enabled 상태로 성공/실패 판단."""
        xpath = XPATH["SUBMIT_NAME"] 

        submit_btn = self.wait_for_element(
        By.XPATH, xpath, 
        condition="clickable", timeout=3
    )
        if not submit_btn:
            logger.error(" 저장 버튼 없음 (DOM에 없음)")
            return False

        #저장 버튼 활성화 여부 먼저 확인
        if not submit_btn.is_enabled():
            logger.error("저장 버튼 비활성화 상태 (저장 불가)")
            return False

        try:
            # 위치 맞추기
            self.driver.execute_script("""
                const rect = arguments[0].getBoundingClientRect();
                const y = rect.top + window.scrollY - 100;
                window.scrollTo({top: y, behavior: 'instant'});
            """, submit_btn)
            self.driver.implicitly_wait(0.3)

            # JS 클릭
            self.driver.execute_script("arguments[0].click();", submit_btn)
            self.driver.implicitly_wait(0.8)

            # 저장 후 다시 '이름' 행으로 스크롤 복귀
            name_row = self.wait_for_element(
                By.XPATH, XPATH["NAME_ROW"], 
                condition="visibility", timeout=3
            )
            if name_row:
                self.driver.execute_script("""
                    const rect = arguments[0].getBoundingClientRect();
                    const y = rect.top + window.scrollY - 120;
                    window.scrollTo({top: y, behavior: 'instant'});
                """, name_row)
            else:
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")

            self.driver.implicitly_wait(0.5)
            logger.info("저장 버튼 JS 클릭 + 이름 행으로 복귀")
            return True

        except Exception as e:
            logger.error(f" 저장 버튼 JS 클릭 실패: {e}")
            return False
    def safe_close(self):
        """테스트 중 안전한 정리 (quit X)"""
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
        except:
            pass
        return True