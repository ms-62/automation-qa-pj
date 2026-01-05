from utils.headers import *

from pages.base_page import BasePage
from utils.defines import  SELECTORS, NAME, XPATH
import time
import logging
    
logger = logging.getLogger()

class MemberPage(BasePage):        
    #우측 사람 이미지 > 계정관리 순차 클릭 > 새 창 이동
    def go_to_member_page(self):
        modal_btn = self.wait_for_element(
            By.CSS_SELECTOR,
            SELECTORS["MEMBER_MODAL"],
            condition="clickable",
            timeout=3)
        self.driver.execute_script("arguments[0].click();", modal_btn) #모달 무조건 스크립트로 클릭

        member_btn = self.wait_for_element(
            By.XPATH,
            XPATH["BTN_MEMBER"],
            condition="clickable",
            timeout=3)
        self.driver.execute_script("arguments[0].click();", member_btn)

        
        self.ensure_account_window()
        return True
    
    #계정 페이지 새로고침
    def refresh_member_account_page(self) -> bool:
        if "accounts.elice.io/members/account" not in self.driver.current_url:
            if not self.go_to_member_page():
                return False
        self.driver.refresh()
        return True

    def scroll_and_interact(self, locator_or_element, offset=120, timeout=5, condition="visibility"):
        """
        인자가 튜플(로케이터)이면 찾고, 이미 요소 객체면 그대로 사용
        """
        if isinstance(locator_or_element, tuple):
            element = self.wait_for_element(*locator_or_element, condition=condition, timeout=timeout)
        else:
            element = locator_or_element
            
        if not element: return None

        # 오프셋 조절 스크롤 실행 (제시해주신 JS 로직 활용)
        self.driver.execute_script(f"""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - {offset};
            window.scrollTo({{top: y, behavior: 'instant'}});
        """, element)
        
        return element

    #이름 관련 테스트 케이스를 위한 메서드
    def open_name_edit_form(self, timeout=5) -> bool:
        logger.info("open_name_edit_form 시작")
        
        # 0) '이름' 행 스크롤 위치 맞추기 공통함수사용
        if not self.scroll_and_interact((By.XPATH,XPATH["NAME_ROW"]), offset=120, timeout=timeout):
            logger.error(" 이름 행을 찾지 못함 (NAME_ROW)")
            return False

        # 1) '이름' 수정 버튼 찾기
        
        edit_btn = self.wait_for_element(By.XPATH,
            XPATH["BTN_NAME_EDIT"],
            offset=120,
            condition="clickable",
            timeout=timeout
            )
        if not edit_btn:
            logger.error("'이름' 수정 버튼 못 찾음 (BTN_NAME_EDIT)")
            return False

        logger.info("'이름' 수정 버튼 찾음, 클릭 시도")

        # JS 클릭 
        self.driver.execute_script("arguments[0].click();", edit_btn)

        # 2) 이름 입력 필드 대기
        input_name = self.wait_for_element(
            By.NAME, 
            NAME["INPUT_NAME"], 
            condition="clickable", 
            check_value=True, # value 속성이 로드될 때까지 내부에서 대기
            timeout=timeout
        )
        
        if not input_name:
            logger.error("이름 수정 폼 열기 실패 (입력 필드 미노출)")
            return False
    
        logger.info("이름 수정 폼 완전 열림")
        return True


    def member_name(self, name) -> bool:
        input_name =  self.wait_for_element(
            By.NAME, 
            NAME["INPUT_NAME"], 
            condition="clickable", 
            check_value=True, # value 속성이 로드될 때까지 내부에서 대기
            timeout=3
        )
        
        if not input_name:
            logger.error("이름 입력란 못 찾음")
            return False

        try:
            input_name.click()
        except Exception as e:
            logger.info(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_name)

        self.driver.execute_script("arguments[0].value = '';", input_name)
        input_name.send_keys(name)

        logger.info(f"테스트 내용 입력 완료: {repr(name)}")
        return True


    def submit_name(self) -> bool:
        """저장 버튼 JS 클릭 + '이름' 행으로 스크롤 복귀 + enabled 상태로 성공/실패 판단."""
        submit_btn = self.scroll_and_interact(
            (By.XPATH, XPATH["SUBMIT_NAME"]), 
            offset=100, 
            timeout=5, 
            condition="clickable"
        )
        
        if not submit_btn:
            logger.error("저장 버튼을 찾지 못함")
            return False

        if not submit_btn.is_enabled():
            logger.error("저장 버튼 비활성화 상태")
            return False

        try:
            # JS 클릭
            self.driver.execute_script("arguments[0].click();", submit_btn)

            # 저장 후 다시 '이름' 행으로 스크롤 복귀
            name_row = self.scroll_and_interact(
                (By.XPATH, XPATH["NAME_ROW"]), 
                offset=120, 
                timeout=3, 
                condition="visibility"
            )
            if not name_row:
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")

            logger.info("저장 버튼 JS 클릭 + 이름 행으로 복귀")
            return True

        except Exception as e:
            logger.error(f" 저장 버튼 JS 클릭 실패: {e}")
            return False
    
    #메일 관련 테스트를 위한 메서드
    def open_email_edit_form(self, timeout=5) -> bool:
        logger.info("open_mail_edit_form 시작")

        # 0) '이메일' 행 스크롤 위치 맞추기
        if not self.scroll_and_interact((By.XPATH,XPATH["EMAIL_ROW"]), offset=120, timeout=timeout):
            logger.error(" 이메일 행을 찾지 못함 (EMAIL_ROW)")
            return False

        # 1) '이메일' 수정 버튼 찾기
        edit_btn = self.wait_for_element(
            By.XPATH,
            XPATH["BTN_EMAIL_EDIT"],
            condition="clickable",
            timeout=timeout,
        )
        if not edit_btn:
            logger.info("'이메일' 수정 버튼 못 찾음 (BTN_EMAIL_EDIT)")
            return False

        logger.info("'이메일' 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        self.driver.execute_script("arguments[0].click();", edit_btn)

        # 2) 이메일 입력 필드 대기
        wait = WebDriverWait(self.driver, timeout)

        input_email = wait.until(EC.presence_of_element_located((
            By.NAME, NAME["INPUT_EMAIL"])))
        
        # 3-2) 입력란 clickable까지 (폼 완전 로딩)
        wait.until(EC.element_to_be_clickable(input_email))
        
        # 3-3) 또는 텍스트/속성 로딩 완료 확인
        wait.until(lambda d: d.find_element(By.NAME, NAME["INPUT_EMAIL"]).get_attribute("value") is not None)
        
        logger.info("이메일 수정 폼 완전 열림")
        return True
    
    def member_email(self, email) -> bool:
        input_email = self.wait_for_element(
            By.NAME,
            NAME["INPUT_EMAIL"], 
            condition="clickable", 
            timeout=3
        )
        if not input_email:
            logger.info("이메일 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_email)

        try:
            input_email.click()
        except Exception as e:
            logger.info(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_email)
            
        self.driver.execute_script("arguments[0].value = '';", input_email)
        input_email.send_keys(email)

        logger.info(f"테스트 내용 입력 완료: {repr(email)}")
        return True
    
    def certification_email(self) -> bool:
        """인증 메일 발송 JS 클릭 + '이메일' 행으로 스크롤 복귀 + enabled 상태가 기본, 실패 테스트: 비활성화가 성공"""
        xpath = XPATH["BTN_CERTI_MAIL"] 

        certi_btn = self.wait_for_element(
            By.XPATH, 
            xpath, 
            condition="clickable", 
            timeout=5,
        )
        if certi_btn:
            logger.info("certification_email: 버튼 clickable 상태")
        else:
            logger.info("certification_email: 버튼 비활성 → 메시지 기준으로만 확인")
        
        base_invalid_elem = self.wait_for_element(
            By.XPATH,
            XPATH["INVALID_MSG"],
            condition="visibility",
            timeout=3,
        )
        base_text = base_invalid_elem.text.strip() if base_invalid_elem else ""
        logger.info(f"certification_email [base] helper-text={repr(base_text)}")

        # 3) 버튼 클릭 시도 (활성일 때만)
        if certi_btn:
            try:
                self.driver.execute_script("arguments[0].click();", certi_btn)
            except Exception as e:
                logger.warning(f"인증메일 버튼 JS 클릭 실패: {e}")
                
        # 클릭 후 다시 이메일 행으로 스크롤 복귀
        email_row = self.wait_for_element(
            By.XPATH, 
            XPATH["EMAIL_ROW"], 
            condition="presence", 
            timeout=3
        )
        if email_row:
            self.driver.execute_script("""
                const rect = arguments[0].getBoundingClientRect();
                const y = rect.top + window.scrollY - 120;
                window.scrollTo({top: y, behavior: 'instant'});
            """, email_row)
        else:
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")
        try:
            input_email = self.wait_for_element(
                By.NAME,
                NAME["INPUT_EMAIL"],
                condition="clickable",
                timeout=3,
            )

            # tooltip 먼저 확보 (공백/형식 오류용)
            tooltip_msg = self.driver.execute_script(
                "return arguments[0].validationMessage;",
                input_email,
            ) or ""
            logger.info(f"certification_email tooltip_msg={repr(tooltip_msg)}")

            if tooltip_msg:
                # 툴팁이 있으면 여기서 끝 (공백/형식 오류 케이스)
                logger.info(tooltip_msg)
                return False

            # helper-text 기반 (중복/횟수 제한용) 기본 문구가 지정되어 있고 인증버튼 클릭 후 변경되는 경우 있음
            base_invalid_elem = self.wait_for_element(
                By.XPATH,
                XPATH["INVALID_MSG"],
                condition="visibility",
                timeout=3,
            )
            base_text = base_invalid_elem.text.strip() if base_invalid_elem else ""
            logger.info(f"certification_email [base] helper-text={repr(base_text)}")

            def helper_text_changed(driver):
                try:
                    elem = driver.find_element(By.XPATH, XPATH["INVALID_MSG"])
                    text = elem.text.strip()
                    # base와 다르고 빈 문자열이 아닐 때만 "변경"으로 인정
                    return text if text and text != base_text else False
                except Exception:
                    return False

            final_invalid_msg = ""
            try:
                changed_text = WebDriverWait(self.driver, 5).until(helper_text_changed)
                final_invalid_msg = changed_text or ""
            except Exception:
                # helper-text가 안 바뀌면 base 텍스트 그대로 사용
                final_invalid_msg = base_text

            logger.info(
                f"certification_email final_invalid_msg={repr(final_invalid_msg)}"
            )

            if final_invalid_msg:
                logger.info(final_invalid_msg)
                return False

            logger.info("인증버튼/상태 정상 (에러 메시지 없음)")
            return True

        except Exception as e:
            logger.error(f"인증메일 발송 후 메시지 확인 실패: {e}")
            return False
    
    #휴대폰 번호 관련 테스트 메서드
    def open_mobile_edit_form(self, timeout=5) -> bool:
        logger.info("open_mobile_edit_form 시작")

        # 0) 휴대폰번호 행 스크롤 위치 맞추기
        mobile_row = self.wait_for_element(
            By.XPATH,
            XPATH["MOBILE_ROW"],
            condition="presence",
            timeout=timeout,
        )
        if not mobile_row:
            logger.info(" 휴대폰 번호 행을 찾지 못함 (MOBILE_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, mobile_row)

        # 1) 휴대폰번호 수정 버튼 찾기
        edit_btn = self.wait_for_element(
            By.XPATH,
            XPATH["BTN_MOBILE_EDIT"],
            condition="visibility",
            timeout=timeout,
        )
        if not edit_btn:
            logger.error("휴대폰번호 수정 버튼 못 찾음 (BTN_MOBILE_EDIT)")
            return False

        logger.info("휴대폰 번호 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        self.driver.execute_script("arguments[0].click();", edit_btn)

        # 2) 휴대폰번호 입력 필드 대기
        input_mobile = self.wait_for_element(
            By.CSS_SELECTOR,
            SELECTORS["INPUT_MOBILE"], 
            condition="visibility", 
            timeout=timeout)
        
        if not input_mobile:
            logger.error("휴대폰 번호 입력란 안 나타남 (폼 안 열림)")
            return False

        logger.info("휴대폰 번호 수정 폼 열림")
        return True
    
    def member_mobile(self, mobile) -> bool:
        input_mobile = self.wait_for_element(
            By.CSS_SELECTOR, 
            SELECTORS["INPUT_MOBILE"], 
            timeout=3, 
            condition="visibility"
        )
        if not input_mobile:
            logger.error("휴대폰 번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_mobile)
        self.driver.implicitly_wait(0.3)

        try:
            input_mobile.click()
        except Exception as e:
            logger.info(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_mobile)

        self.driver.execute_script("arguments[0].value = '';", input_mobile)
        input_mobile.send_keys(mobile)

        logger.info(f"테스트 내용 입력 완료: {repr(mobile)}")
        return True
    
    def certification_mobile(self) -> bool:
        """4시간 내 최대 5회 발송 시도 후 확인"""
        certi_btn = self.wait_for_element(
            By.XPATH, 
            XPATH["BTN_CERTI_MOBIL"],
            timeout=5,
            condition="clickable")
        
        if not certi_btn:
            logger.error("인증 문자 버튼 없음 (DOM에 없음)")
            return False
        
        click_attempts = 0
        max_attempts = 6
        server_responses = 0  # 서버 실제 반응 횟수 추적
        
        try:
            while click_attempts < max_attempts:
                click_attempts += 1
                logger.info(f"클릭 {click_attempts}/{max_attempts}")
                
                self.driver.execute_script("arguments[0].click();", certi_btn)
                
                # 점진적 대기 wait으로 서버 응답 대기 횟수가 차이나서 time.sleep() 사용
                wait_time = 1.8 + (click_attempts * 0.1)  
                time.sleep(wait_time)
                
                # 서버 응답 확인 (토스트/버튼 상태 변화)
                try:
                    toast = self.driver.find_element(By.XPATH, XPATH["TOAST_CONTAINER"])
                    if toast.is_displayed() and toast.text.strip():
                        server_responses += 1
                        logger.info(f"서버 응답 #{server_responses}: {toast.text.strip()}")
                        time.sleep(0.3)  # 토스트 읽고 난 후 추가 대기
                except:
                    pass  # 토스트 없음 = 서버 무시
                
                # 스크롤 복귀 (생략)
            
            logger.info(f"클릭:{click_attempts}회, 서버응답:{server_responses}회")
            
            # 최대 횟수 초과 토스트 대기
            wait = WebDriverWait(self.driver, 10)
            toast_xpath = XPATH["TOAST_CONTAINER"]
            wait.until(EC.visibility_of_element_located((By.XPATH, toast_xpath)))
            
            toast_msg = self.driver.find_element(By.XPATH, toast_xpath).text.strip()
            logger.info(f"최종 토스트: {repr(toast_msg)}")
            
            return "최대" in toast_msg or "5회" in toast_msg
            
        except Exception as e:
            logger.error(f"실패: {e}")
            return False
        
    #비밀번호 관련 테스트 메서드
    def open_pwd_edit_form(self, timeout=5) -> bool:
        logger.info("open_pwd_edit_form 시작")

        # 0) 비밀번호 행 스크롤 위치 맞추기
        pwd_row = self.wait_for_element(
            By.XPATH,
            XPATH["PWD_ROW"],
            condition="presence",
            timeout=timeout,
        )
        if not pwd_row:
            logger.error(" 비밀번호 행을 찾지 못함 (PWD_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, pwd_row)

        # 1) 비밀번호 수정 버튼 찾기
        edit_btn = self.wait_for_element(
            By.XPATH,
            XPATH["BTN_PWD_EDIT"],
            condition="clickable",
            timeout=timeout,
        )
        if not edit_btn:
            logger.error("비밀번호 수정 버튼 못 찾음 (BTN_PWD_EDIT)")
            return False

        logger.info("비밀번호 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        self.driver.execute_script("arguments[0].click();", edit_btn)


        # 2) 비밀번호 입력 필드 대기
        input_pwd = self.wait_for_element(
            By.NAME,
            NAME["INPUT_PWD"],
            condition="clickable",
            timeout=timeout)
        if not input_pwd:
            logger.error("비밀번호 입력란 안 나타남 (폼 안 열림)")
            return False

        logger.info("비밀번호 수정 폼 열림")
        return True
    
    def member_fail_pwd(self, pwd) -> bool:
        input_pwd = self.wait_for_element(
            By.NAME,
            NAME["INPUT_PWD"], 
            condition="clickable",
            timeout=3)
        input_new_pwd = self.wait_for_element(
            By.NAME,
            NAME["INPUT_NEW_PWD"],
            condition="clickable",
            timeout=3)
        
        if not input_pwd:
            logger.error("비밀번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_pwd)
        
        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_new_pwd)

        try:
            input_pwd.click()
            input_new_pwd.click()
        except Exception as e:
            logger.info(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_pwd)
            self.driver.execute_script("arguments[0].focus();", input_new_pwd)

        self.driver.execute_script("arguments[0].value = '';", input_pwd)
        self.driver.execute_script("arguments[0].value = '';", input_new_pwd)
        input_pwd.send_keys(pwd)
        input_new_pwd.send_keys(pwd)

        logger.info(f"비밀번호 입력 완료: {repr(pwd)}")
        return True
    
    def change_fail_pwd(self) -> bool :
        """동일한 비밀번호 기입한 상태로 변경 시도 : 테스트 내용 실패가 성공"""
        submit_pwd = self.wait_for_element(
            By.XPATH,
            XPATH["SUBMIT_PWD"] , 
            condition="clickable",
            timeout=3)
        
        if not submit_pwd:
            logger.error("완료 버튼 없음 (DOM에 없음)")
            return False
        try:
            self.driver.execute_script("arguments[0].click();", submit_pwd)

            invalid_msg = self.wait_for_element(
                By.XPATH,
                XPATH["INVALID_MSG"],
                condition="visibility",
                timeout=4).text
            
            if invalid_msg:
                logger.error(f"비밀번호 변경 실패 : {invalid_msg}")
                return False
            else:
                logger.info("비번 변경됨")
                return True
            
        except Exception as e:
            logger.error(f"예외 발생: {e}")
            return False
    
    def member_success_pwd(self, pwd , pwd_new) -> bool:
        input_pwd = self.wait_for_element(
            By.NAME,
            NAME["INPUT_PWD"],
            condition="clickable",
            timeout=3)
        input_new_pwd = self.wait_for_element(
            By.NAME,
            NAME["INPUT_NEW_PWD"],
            condition="clickable",
            timeout=3)
        
        if not input_pwd:
            logger.error("비밀번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_pwd)
        
        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_new_pwd)

        try:
            input_pwd.click()
            input_new_pwd.click()
        except Exception as e:
            logger.info(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_pwd)
            self.driver.execute_script("arguments[0].focus();", input_new_pwd)

        self.driver.execute_script("arguments[0].value = '';", input_pwd)
        self.driver.execute_script("arguments[0].value = '';", input_new_pwd)
        input_pwd.send_keys(pwd)
        input_new_pwd.send_keys(pwd_new)

        self.driver.implicitly_wait(0.5)
        logger.info(f"기존 비밀번호 입력 완료: {repr(pwd)}")
        logger.info(f"신규 비밀번호 입력 완료: {repr(pwd_new)}")
        return True
    
    def change_success_pwd(self) -> bool:
        """비밀번호 변경 성공"""
        submit_pwd = self.wait_for_element(
            By.XPATH,
            XPATH["SUBMIT_PWD"] ,
            condition="clickable",
            timeout=3)
        
        if not submit_pwd:
            logger.error("완료 버튼 없음 (DOM에 없음)")
            return False
        try:
            self.driver.execute_script("arguments[0].click();", submit_pwd)

            #toast 문구 확인
            toast_container = self.wait_for_element(
                By.XPATH,
                XPATH["TOAST_CONTAINER"],
                condition="visibility",
                timeout=5 )
            
            toast_msg = toast_container.text
            if toast_msg:
                logger.info(f"비밀번호 변경 성공 : {toast_msg}")
                return True
            else:
                logger.error("비밀빈호 변경 실패")
                return False
            
        except Exception as e:
            logger.warning(f"예외 발생: {e}")
            return False
    
    #선호 언어 변경 메서드
    def open_lang_edit_form(self, timeout=5) -> bool:
        logger.info("open_lang_edit_form 시작")

        # 0) 선호언어 행 스크롤 위치 맞추기
        lang_row = self.wait_for_element(
            By.XPATH,
            XPATH["LANG_ROW"],
            condition="presence",
            timeout=timeout,
        )
        if not lang_row:
            logger.error(" 선호 언어 행을 찾지 못함 (LANG_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, lang_row)
        logger.info("선호 언어 행 찾음")
        return True
        
    def choose_lang_dropbox(self) -> bool:
        lang_box = self.wait_for_element(
            By.XPATH,
            XPATH["BOX_LANG"],
            condition="visibility",
            timeout=3)
        lang_box.click()
        
        logger.info("선호 언어 행 클릭")
        choose_eng =  self.wait_for_element(
            By.CSS_SELECTOR,
            SELECTORS["BOX_LANG_ENG"],
            condition="clickable",
            timeout=3)
        choose_eng.click()
        return choose_eng
    
    def choose_lang_check(self) -> bool: #언어변경 확인을 위한 계정관리 창 종료 후 다시 접속
        try:
            handles = self.driver.window_handles
            if not handles:
                logger.error("choose_lang_check: 윈도우 핸들이 없음")
                return False
            #현재창종료
            current_handle = self.driver.current_window_handle
            logger.info(f"choose_lang_check: current_handle={current_handle}")
            self.driver.close()

            remaining_handles = self.driver.window_handles
            if not remaining_handles:
                logger.error("choose_lang_check: close 후 남은 창이 없음")
                return False

            main_handle = remaining_handles[0]
            self.driver.switch_to.window(main_handle)
            logger.info(f"choose_lang_check: main_handle={main_handle}")

            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.find_element(By.TAG_NAME, "body")
                )
            except Exception:
                pass  # 로딩이 조금 느려도 아래에서 다시 URL/요소로 검증
            self.go_to_member_page()
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.url_contains("lang=en-US")
                )
            except Exception:
                pass

            current_url = self.driver.current_url
            logger.info(f"choose_lang_check: 최종 URL={current_url}")

            if "lang=en-US" in current_url:
                logger.info("선호 언어 변경 성공")
                return True
            else:
                logger.error(f"선호 언어 변경 실패: {current_url}")
                return False

        except Exception as e:
            logger.error(f"choose_lang_check 예외 발생: {e}")
            return False
    
    def revoke_lang_kor(self) -> bool:
        handles = self.driver.window_handles
        if not handles:
            logger.error("revoke_lang_kor: 윈도우 핸들이 없음")
            return False

        original_window = handles[0]

        # 언어 드롭박스
        lang_box = self.wait_for_element(
            By.XPATH,
            XPATH["BOX_LANG"],
            condition="clickable",  
            timeout=5,
        )
        if not lang_box:
            logger.error("revoke_lang_kor: 언어 드롭박스 못 찾음")
            return False

        lang_box.click()
        logger.info("선호 언어 행 클릭")

        #  한국어 옵션 (드롭다운 열리고 나서 클릭 가능 상태까지)
        choose_kor = self.wait_for_element(
            By.CSS_SELECTOR,
            SELECTORS["BOX_LANG_KOR"],
            condition="clickable",
            timeout=5,
        )
        if not choose_kor:
            logger.error("revoke_lang_kor: 한국어 옵션 못 찾음")
            return False

        choose_kor.click()
        logger.info("한국어 옵션 선택")

        # 3) 현재 창 닫기
        self.driver.close()

        # 4) 남은 창으로 전환 + 로딩 짧게 대기
        remaining_handles = self.driver.window_handles
        self.wait_for_page_load()
        if not remaining_handles:
            logger.error("revoke_lang_kor: close 후 남은 창이 없음")
            return False
        try:
            social_row = self.wait_for_element(By.XPATH, XPATH["SOCIAL_ROW"], timeout=5)
            self.driver.execute_script("arguments[0].scrollIntoView();", social_row)
            logger.info("revoke_lang_kor 성공")
            return True
        except:
            logger.warning("OAuth 영역 대기 실패 - 기본 페이지 로드만 완료")
            return True

    #oauth 계정 연동 테스트 메서드
    OAUTH_PROVIDERS = [
    ("BTN_OAUTH_NAVER", "Naver"), 
    ("BTN_OAUTH_KKO", "Kakao"),
    ("BTN_OAUTH_GITHUB", "GitHub"),
    ("BTN_OAUTH_WHALESPACE", "Whalespace"),
    ("BTN_OAUTH_APPLE", "Apple"),
    ("BTN_OAUTH_FACEBOOK", "Facebook"),
    ("BTN_OAUTH_MICROSOFT", "Microsoft"),
    ("BTN_OAUTH_GOOGLE", "Google"),

]   

    def click_oauth_provider(self, xpath_key: str, provider_name: str) -> bool:
        """OAuth 버튼 클릭만 (스크롤 + 클릭 + 팝업)"""
        logger.info(f"=== {provider_name} 전체 과정 추적 ===")
        success = False  # 변수 초기화
    
        try:
            #Window 복구
            handles = self.driver.window_handles
            if handles:
                self.driver.switch_to.window(handles[0])
            else:
                logger.warning("빈 handles → 새로고침!")
                self.driver.refresh()
            
            if "members/account" not in self.driver.current_url:
                logger.info("계정관리페이지 재접속!")
                self.driver.get("https://accounts.elice.io/members/account")  # 직접 URL
                
            # 소셜 영역
            social_row = self.wait_for_element(By.XPATH, XPATH["SOCIAL_ROW"], timeout=10)
            self.driver.execute_script("arguments[0].scrollIntoView();", social_row)
            
            # 버튼
            btn_xpath = XPATH[xpath_key]
            btn = self.wait_for_element(By.XPATH, btn_xpath, condition="clickable", timeout=15)
            self.driver.execute_script("arguments[0].click();", btn)
            def button_clicked(driver):
                try:
                    updated_btn = driver.find_element(By.XPATH, btn_xpath)
                    # 클릭 후 disabled 또는 loading 상태 확인
                    return (updated_btn.get_attribute("disabled") or 
                        "loading" in updated_btn.get_attribute("class").lower() or
                        not updated_btn.is_enabled())
                except:
                    return False
            def popup_opened(driver):
                return len(driver.window_handles) > 1
            
            # 병렬 대기: 버튼 변화 OR 팝업 열림
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda d: button_clicked(d) or popup_opened(d)
                )
                logger.info(f"클릭 성공! handles: {len(self.driver.window_handles)}")
            except:
                logger.warning(f"⚠️ {provider_name} 클릭 느림 - 계속 진행")
            success = self.oauth_popup_open_close()
            
            logger.info(f"=== {provider_name} 종료 ===")
        except Exception as e:
            logger.error(f"팝업 오픈 실패: {e}")
        return success

    def oauth_popup_open_close(self) -> bool:
        """OAuth 팝업 안전 정리 + 계정관리페이지 확실 복귀"""
        logger.info("OAuth 팝업 정리 시작")
        
        handles = self.driver.window_handles
        
        if len(handles) <= 1:
            logger.warning("팝업 없음 - 정리 불필요")
            return False
        
        try:
            original_account_window = handles[0]  #항상 첫 번째 창 고정
            self.driver.switch_to.window(original_account_window)
            logger.info(f"원본 창 확보: {original_account_window[:8]}")
        except:
            logger.error(" 원본 창 접근 실패!")
            return False
        
        #OAuth 팝업만 정리
        oauth_patterns = ["login", "oauth", "signin", "auth", "nid.naver", "accounts.google", "kakao", "github", "facebook", "appleid", "microsoftonline", "worksmobile"]
        current_handles = self.driver.window_handles[:]  # 복사본
        for handle in current_handles:
            if handle == original_account_window:
                continue
                
            try:
                self.driver.switch_to.window(handle)
                current_url = self.driver.current_url
                
                for pattern in oauth_patterns:
                    if pattern in current_url.lower():
                        logger.info(f"연동 팝업 발견: {current_url[:50]}")
                        self.driver.close()
                        logger.info("팝업 창 종료")
                        break
            except:
                continue  # 안전하게 스킵
        
        #원본 창으로 복귀 + 검증
        try:
            self.driver.switch_to.window(original_account_window)
            
            # 최종 검증
            final_handles = len(self.driver.window_handles)
            final_url_ok = "members/account" in self.driver.current_url
            
            if final_handles == 1 and final_url_ok:
                logger.info("팝업 종료 완료")
                return True
            else:
                logger.error(f"정리 실패 - handles: {final_handles}, URL: {self.driver.current_url[:50]}")
                return False
                
        except Exception as e:
            logger.error(f" 복귀 실패: {e}")
            return False