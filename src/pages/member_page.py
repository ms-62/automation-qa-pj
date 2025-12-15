from utils.headers import *

from pages.base_page import BasePage
from utils.defines import TARGET_URL, SELECTORS, NAME, XPATH

class MemberPage(BasePage):
    #로그인 > 메인 페이지 이동
    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
        time.sleep(4) 

    #우측 사람 이미지 > 계정관리 순차 클릭 > 새 창 이동
    def go_to_member_page(self):
        modal_btn = self.get_element_by_css_selector(SELECTORS["MEMBER_MODAL"])
        self.driver.execute_script("arguments[0].click();", modal_btn) #모달 무조건 스크립트로 클릭
        time.sleep(4)
        member_btn = self.get_element_by_xpath(XPATH["BTN_MEMBER"])
        self.driver.execute_script("arguments[0].click();", member_btn)
        time.sleep(4)
        
        self.ensure_account_window()
        return True
    
    #계정 페이지 새로고침
    def refresh_member_account_page(self):
        if "accounts.elice.io/members/account" not in self.driver.current_url:
            if not self.go_to_member_page():
                return False
        self.driver.refresh()
        time.sleep(3)
        return True

    #이름 관련 테스트 케이스를 위한 메서드
    def open_name_edit_form(self, timeout=5):
        print("open_name_edit_form 시작")

        # 0) '이름' 행 스크롤 위치 맞추기
        name_row = self.get_element(
            By.XPATH,
            XPATH["NAME_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not name_row:
            print(" '이름' 행을 찾지 못함 (NAME_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, name_row)
        time.sleep(0.3)

        # 1) '이름' 수정 버튼 찾기
        edit_btn = self.get_element(
            By.XPATH,
            XPATH["BTN_NAME_EDIT"],
            option="visibility",
            timeout=timeout,
        )
        if not edit_btn:
            print("'이름' 수정 버튼 못 찾음 (BTN_NAME_EDIT)")
            return False

        print("'이름' 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭 
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.5)

        # 2) 이름 입력 필드 대기
        input_name = self.get_element_by_name(NAME["INPUT_NAME"], option="visibility", timeout=timeout)
        if not input_name:
            print("이름 입력란 안 나타남 (폼 안 열림)")
            return False

        print("이름 수정 폼 열림")
        return True


    def member_name(self, name):
        input_name = self.get_element_by_name(NAME["INPUT_NAME"], option="visibility", timeout=3)
        if not input_name:
            print("이름 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_name)
        time.sleep(0.3)

        try:
            input_name.click()
        except Exception as e:
            print(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_name)

        self.driver.execute_script("arguments[0].value = '';", input_name)
        input_name.send_keys(name)

        time.sleep(0.5)
        print(f"테스트 내용 입력 완료: {repr(name)}")
        return True


    def submit_name(self):
        """저장 버튼 JS 클릭 + '이름' 행으로 스크롤 복귀 + enabled 상태로 성공/실패 판단."""
        xpath = XPATH["SUBMIT_NAME"] 

        submit_btn = self.get_element(By.XPATH, xpath, option="visibility", timeout=3)
        if not submit_btn:
            print(" 저장 버튼 없음 (DOM에 없음)")
            return False

        #저장 버튼 활성화 여부 먼저 확인
        if not submit_btn.is_enabled():
            print("저장 버튼 비활성화 상태 (저장 불가)")
            return False

        try:
            # 위치 맞추기
            self.driver.execute_script("""
                const rect = arguments[0].getBoundingClientRect();
                const y = rect.top + window.scrollY - 100;
                window.scrollTo({top: y, behavior: 'instant'});
            """, submit_btn)
            time.sleep(0.3)

            # JS 클릭
            self.driver.execute_script("arguments[0].click();", submit_btn)
            time.sleep(0.8)

            # 저장 후 다시 '이름' 행으로 스크롤 복귀
            name_row = self.get_element(By.XPATH, XPATH["NAME_ROW"], option="presence", timeout=3)
            if name_row:
                self.driver.execute_script("""
                    const rect = arguments[0].getBoundingClientRect();
                    const y = rect.top + window.scrollY - 120;
                    window.scrollTo({top: y, behavior: 'instant'});
                """, name_row)
            else:
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")

            time.sleep(0.5)
            print("저장 버튼 JS 클릭 + 이름 행으로 복귀")
            return True

        except Exception as e:
            print(f" 저장 버튼 JS 클릭 실패: {e}")
            return False
    
    #메일 관련 테스트를 위한 메서드
    def open_email_edit_form(self, timeout=5):
        print("open_mail_edit_form 시작")

        # 0) '이메일' 행 스크롤 위치 맞추기
        email_row = self.get_element(
            By.XPATH,
            XPATH["EMAIL_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not email_row:
            print(" 이메일 행을 찾지 못함 (EMAIL_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, email_row)
        time.sleep(0.3)

        # 1) '이메일' 수정 버튼 찾기
        edit_btn = self.get_element(
            By.XPATH,
            XPATH["BTN_EMAIL_EDIT"],
            option="visibility",
            timeout=timeout,
        )
        if not edit_btn:
            print("'이메일' 수정 버튼 못 찾음 (BTN_EMAIL_EDIT)")
            return False

        print("'이메일' 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.5)

        # 2) 이메일 입력 필드 대기
        input_email = self.get_element_by_name(NAME["INPUT_EMAIL"], option="visibility", timeout=timeout)
        if not input_email:
            print("이메일 입력란 안 나타남 (폼 안 열림)")
            return False

        print("이메일 수정 폼 열림")
        return True
    
    def member_email(self, email):
        input_email = self.get_element_by_name(NAME["INPUT_EMAIL"], option="visibility", timeout=3)
        if not input_email:
            print("이메일 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_email)
        time.sleep(0.3)

        try:
            input_email.click()
        except Exception as e:
            print(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_email)

        self.driver.execute_script("arguments[0].value = '';", input_email)
        input_email.send_keys(email)

        time.sleep(0.5)
        print(f"테스트 내용 입력 완료: {repr(email)}")
        return True
    
    def certification_email(self):
        """인증 메일 발송 JS 클릭 + '이메일' 행으로 스크롤 복귀 + enabled 상태가 기본, 실패 테스트: 비활성화가 성공"""
        xpath = XPATH["BTN_CERTI_MAIL"] 

        certi_btn = self.get_element(By.XPATH, xpath, option="visibility", timeout=3)
        if not certi_btn:
            print(" 인증메일 발송 버튼 없음 (DOM에 없음)")
            return False
        try:
            # JS 클릭 - 중복 이메일만 클릭 가능
            self.driver.execute_script("arguments[0].click();", certi_btn)
            time.sleep(0.8)
            
            # 클릭 후 다시 이메일 행으로 스크롤 복귀
            email_row = self.get_element(By.XPATH, XPATH["EMAIL_ROW"], option="presence", timeout=3)
            if email_row:
                self.driver.execute_script("""
                    const rect = arguments[0].getBoundingClientRect();
                    const y = rect.top + window.scrollY - 120;
                    window.scrollTo({top: y, behavior: 'instant'});
                """, email_row)
            else:
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")
            
            input_email = self.get_element_by_name(NAME["INPUT_EMAIL"], option="visibility", timeout=3)
            tooltip_msg = self.driver.execute_script("return arguments[0].validationMessage;", input_email)
            invalid_msg = self.get_element_by_xpath(XPATH["INVALID_MSG"]).text
            
            if tooltip_msg : #msg가 존재하면 출력
                    print(tooltip_msg)
                    return False
            elif invalid_msg:
                    print(invalid_msg)
                    return False
            else:
                print("인증버튼 클릭 성공")
                return True
                
        except Exception as e:
            print(f" 인증메일 발송 버튼 JS 클릭 실패: {e}")
            return False
    
    #휴대폰 번호 관련 테스트 메서드
    def open_mobile_edit_form(self, timeout=5):
        print("open_mobile_edit_form 시작")

        # 0) 휴대폰번호 행 스크롤 위치 맞추기
        mobile_row = self.get_element(
            By.XPATH,
            XPATH["MOBILE_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not mobile_row:
            print(" 휴대폰 번호 행을 찾지 못함 (MOBILE_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, mobile_row)
        time.sleep(0.3)

        # 1) 휴대폰번호 수정 버튼 찾기
        edit_btn = self.get_element(
            By.XPATH,
            XPATH["BTN_MOBILE_EDIT"],
            option="visibility",
            timeout=timeout,
        )
        if not edit_btn:
            print("휴대폰번호 수정 버튼 못 찾음 (BTN_MOBILE_EDIT)")
            return False

        print("휴대폰 번호 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.5)

        # 2) 휴대폰번호 입력 필드 대기
        input_mobile = self.get_element_by_css_selector(SELECTORS["INPUT_MOBILE"], option="visibility", timeout=timeout)
        if not input_mobile:
            print("휴대폰 번호 입력란 안 나타남 (폼 안 열림)")
            return False

        print("휴대폰 번호 수정 폼 열림")
        return True
    
    def member_mobile(self, mobile):
        input_mobile = self.get_element_by_css_selector(SELECTORS["INPUT_MOBILE"], option="visibility", timeout=3)
        if not input_mobile:
            print("휴대폰 번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_mobile)
        time.sleep(0.3)

        try:
            input_mobile.click()
        except Exception as e:
            print(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_mobile)

        self.driver.execute_script("arguments[0].value = '';", input_mobile)
        input_mobile.send_keys(mobile)

        time.sleep(0.5)
        print(f"테스트 내용 입력 완료: {repr(mobile)}")
        return True
    
    def certification_mobile(self):
        """4시간 내 최대 5회 발송 시도 후 확인"""
        certi_btn = self.get_element(By.XPATH, XPATH["BTN_CERTI_MOBIL"] , option="visibility", timeout=3)
        if not certi_btn:
            print("인증 문자 버튼 없음 (DOM에 없음)")
            return False
        try:
            for i in range(6):
                print(f"인증 버튼 {i+1}/5 클릭 시도")
                self.driver.execute_script("arguments[0].click();", certi_btn)
                time.sleep(0.8)
                
                # 클릭 후 다시 휴대폰 번호 행으로 스크롤 복귀
                email_row = self.get_element(By.XPATH, XPATH["EMAIL_ROW"], option="presence", timeout=3)
                if email_row:
                    self.driver.execute_script("""
                        const rect = arguments[0].getBoundingClientRect();
                        const y = rect.top + window.scrollY - 120;
                        window.scrollTo({top: y, behavior: 'instant'});
                    """, email_row)
                else:
                    self.driver.execute_script("window.scrollTo({top: 0, behavior: 'instant'});")
            print("인증 버튼 5회 연속 클릭 완료")
            
            #toast 문구 확인
            toast_container = self.get_element(By.XPATH,XPATH["TOAST_CONTAINER"],option="visibility", timeout=5 )
            toast_msg = toast_container.text
            print(toast_msg)
            return True
                
        except Exception as e:
            print(f"인증발송 최대횟수 시도 후 토스트 확인 실패: {e}")
            return False
        
    #비밀번호 관련 테스트 메서드
    def open_pwd_edit_form(self, timeout=5):
        print("open_pwd_edit_form 시작")

        # 0) 비밀번호 행 스크롤 위치 맞추기
        pwd_row = self.get_element(
            By.XPATH,
            XPATH["PWD_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not pwd_row:
            print(" 비밀번호 행을 찾지 못함 (PWD_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, pwd_row)
        time.sleep(0.3)

        # 1) 비밀번호 수정 버튼 찾기
        edit_btn = self.get_element(
            By.XPATH,
            XPATH["BTN_PWD_EDIT"],
            option="visibility",
            timeout=timeout,
        )
        if not edit_btn:
            print("비밀번호 수정 버튼 못 찾음 (BTN_PWD_EDIT)")
            return False

        print("비밀번호 수정 버튼 찾음, 클릭 시도")

        # 스크롤 + JS 클릭
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        time.sleep(0.3)
        self.driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(0.5)

        # 2) 비밀번호 입력 필드 대기
        input_pwd = self.get_element_by_name(NAME["INPUT_PWD"], option="visibility", timeout=timeout)
        if not input_pwd:
            print("비밀번호 입력란 안 나타남 (폼 안 열림)")
            return False

        print("비밀번호 수정 폼 열림")
        return True
    
    def member_fail_pwd(self, pwd):
        input_pwd = self.get_element_by_name(NAME["INPUT_PWD"], option="visibility", timeout=3)
        input_new_pwd = self.get_element_by_name(NAME["INPUT_NEW_PWD"], option="visibility", timeout=3)
        
        if not input_pwd:
            print("비밀번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_pwd)
        time.sleep(0.3)
        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_new_pwd)
        time.sleep(0.3)

        try:
            input_pwd.click()
            input_new_pwd.click()
        except Exception as e:
            print(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_pwd)
            self.driver.execute_script("arguments[0].focus();", input_new_pwd)

        self.driver.execute_script("arguments[0].value = '';", input_pwd)
        self.driver.execute_script("arguments[0].value = '';", input_new_pwd)
        input_pwd.send_keys(pwd)
        input_new_pwd.send_keys(pwd)

        time.sleep(0.5)
        print(f"비밀번호 입력 완료: {repr(pwd)}")
        return True
    
    def change_fail_pwd(self):
        """동일한 비밀번호 기입한 상태로 변경 시도 : 테스트 내용 실패가 성공"""
        submit_pwd = self.get_element(By.XPATH, XPATH["SUBMIT_PWD"] , option="visibility", timeout=3)
        if not submit_pwd:
            print("완료 버튼 없음 (DOM에 없음)")
            return False
        try:
            self.driver.execute_script("arguments[0].click();", submit_pwd)
            time.sleep(0.8)

            invalid_msg = self.get_element_by_xpath(XPATH["INVALID_MSG"]).text
            
            if invalid_msg:
                print(f"비밀번호 변경 실패 : {invalid_msg}")
                return False
            else:
                print("비번 변경됨")
                return True
            
        except Exception as e:
            print(f"예외 발생: {e}")
            return False
    
    def member_success_pwd(self, pwd , pwd_new):
        input_pwd = self.get_element_by_name(NAME["INPUT_PWD"], option="visibility", timeout=3)
        input_new_pwd = self.get_element_by_name(NAME["INPUT_NEW_PWD"], option="visibility", timeout=3)
        
        if not input_pwd:
            print("비밀번호 입력란 못 찾음")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_pwd)
        time.sleep(0.3)
        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 100;
            window.scrollTo({top: y, behavior: 'instant'});
        """, input_new_pwd)
        time.sleep(0.3)

        try:
            input_pwd.click()
            input_new_pwd.click()
        except Exception as e:
            print(f"input 클릭 실패: {e}")
            self.driver.execute_script("arguments[0].focus();", input_pwd)
            self.driver.execute_script("arguments[0].focus();", input_new_pwd)

        self.driver.execute_script("arguments[0].value = '';", input_pwd)
        self.driver.execute_script("arguments[0].value = '';", input_new_pwd)
        input_pwd.send_keys(pwd)
        input_new_pwd.send_keys(pwd_new)

        time.sleep(0.5)
        print(f"기존 비밀번호 입력 완료: {repr(pwd)}")
        print(f"신규 비밀번호 입력 완료: {repr(pwd_new)}")
        return True
    
    def change_success_pwd(self):
        """비밀번호 변경 성공"""
        submit_pwd = self.get_element(By.XPATH, XPATH["SUBMIT_PWD"] , option="visibility", timeout=3)
        if not submit_pwd:
            print("완료 버튼 없음 (DOM에 없음)")
            return False
        try:
            self.driver.execute_script("arguments[0].click();", submit_pwd)
            time.sleep(0.8)

            #toast 문구 확인
            toast_container = self.get_element(By.XPATH,XPATH["TOAST_CONTAINER"],option="visibility", timeout=5 )
            toast_msg = toast_container.text
            if toast_msg:
                print(f"비밀번호 변경성공 : {toast_msg}")
                return True
            else:
                print("비밀빈호 변경 실패")
                return False
            
        except Exception as e:
            print(f"예외 발생: {e}")
            return False
    
    #선호 언어 변경 메서드
    def open_lang_edit_form(self, timeout=5):
        print("open_lang_edit_form 시작")

        # 0) 선호언어 행 스크롤 위치 맞추기
        lang_row = self.get_element(
            By.XPATH,
            XPATH["LANG_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not lang_row:
            print(" 선호 언어 행을 찾지 못함 (LANG_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, lang_row)
        time.sleep(0.3)
        print("선호 언어 행 찾음")
        return True
        
    def choose_lang_dropbox(self):
        lang_box = self.get_element_by_xpath(XPATH["BOX_LANG"])
        lang_box.click()
        time.sleep(2)
        print("선호 언어 행 클릭")
        
        choose_eng =  self.get_element_by_css_selector(SELECTORS["BOX_LANG_ENG"])
        choose_eng.click()
        time.sleep(2)
        return True
    
    def choose_lang_check(self): #언어변경 확인을 위한 계정관리 창 종료 후 다시 접속
        handles = self.driver.window_handles
        original_window = handles[0] 
        self.driver.close()
        self.driver.switch_to.window(original_window)
        self.go_to_member_page()
        print("계정 창 돌아와서 언어 변경 확인")
        return True
    
    def revoke_lang_kor(self):
        handles = self.driver.window_handles
        original_window = handles[0] 
        #다음 테스트를 위한 한국어 변경
        lang_box = self.get_element_by_xpath(XPATH["BOX_LANG"])
        lang_box.click()
        time.sleep(2)
        print("선호 언어 행 클릭")
        
        choose_kor =  self.get_element_by_css_selector(SELECTORS["BOX_LANG_KOR"])
        choose_kor.click()
        self.driver.close()
        self.driver.switch_to.window(original_window)
        self.go_to_member_page()
        print("한국어 원복")
        return True
        
    #oauth 계정 연동 테스트 메서드
    def open_oauth_edit_form(self, timeout=5):
        print("open_oauth_edit_form 시작")

        # 0) 선호언어 행 스크롤 위치 맞추기
        social_row = self.get_element(
            By.XPATH,
            XPATH["SOCIAL_ROW"],
            option="presence",
            timeout=timeout,
        )
        if not social_row:
            print(" 소셜 계정 연동 행을 찾지 못함 (SOCIAL_ROW)")
            return False

        self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            const y = rect.top + window.scrollY - 120;
            window.scrollTo({top: y, behavior: 'instant'});
        """, social_row)
        time.sleep(0.3)
        print("소셜 계정 연동 행 찾음")
        return True
    
    def oauth_google_click(self):
        btn_oauth_google = self.get_element_by_xpath(XPATH["BTN_OAUTH_GOOGLE"])
        btn_oauth_google.click()
        time.sleep(4)
        print("구글 연결하기 클릭")
        return True
    
    def oauth_naver_click(self):
        btn_oauth_naver = self.get_element_by_xpath(XPATH["BTN_OAUTH_NAVER"])
        btn_oauth_naver.click()
        time.sleep(4)
        print("네이버 연결하기 클릭")
        return True

    def oauth_kko_click(self):
        btn_oauth_kko = self.get_element_by_xpath(XPATH["BTN_OAUTH_KKO"])
        btn_oauth_kko.click()
        time.sleep(4)
        print("카카오 연결하기 클릭")
        self.oauth_popup_open_close()
        return True
    
    def oauth_github_click(self):
        btn_oauth_github = self.get_element_by_xpath(XPATH["BTN_OAUTH_GITHUB"])
        btn_oauth_github.click()
        time.sleep(4)
        print("깃허브 연결하기 클릭")
        self.oauth_popup_open_close()
        return True

    def oauth_apple_click(self):
        btn_oauth_apple = self.get_element_by_xpath(XPATH["BTN_OAUTH_APPLE"])
        btn_oauth_apple.click()
        time.sleep(7)
        print("애플 연결하기 클릭")
        self.oauth_popup_open_close()
        return True
    
    def oauth_facebook_click(self):
        btn_oauth_facebook = self.get_element_by_xpath(XPATH["BTN_OAUTH_FACEBOOK"])
        btn_oauth_facebook.click()
        time.sleep(4)
        print("페이스북 연결하기 클릭")
        self.oauth_popup_open_close()
        return True

    def oauth_whalespace_click(self):
        btn_oauth_whalespace = self.get_element_by_xpath(XPATH["BTN_OAUTH_WHALESPACE"])
        btn_oauth_whalespace.click()
        time.sleep(4)
        print("웨일스페이스 연결하기 클릭")
        self.oauth_popup_open_close()
        return True
    
    def oauth_microsoft_click(self):
        btn_oauth_microsoft = self.get_element_by_xpath(XPATH["BTN_OAUTH_MICROSOFT"])
        btn_oauth_microsoft.click()
        time.sleep(4)
        print("마이크로소프트 연결하기 클릭")
        self.oauth_popup_open_close()
        return True    
        
    def oauth_popup_open_close(self):
        handles = self.driver.window_handles
        original_account_window = handles[1] #계정관리창 순서 고정해서 찾기
        # 연동 관련 페이지 URL 패턴
        oauth_patterns = ["login", "oauth", "signin","auth"]
        
        for handle in handles:
            self.driver.switch_to.window(handle) #팝업으로 전환
            current_url = self.driver.current_url
            
            for pattern in oauth_patterns:
                if pattern in current_url:
                    print(f"연동 팝업 발견: {current_url[:50]}")
                    self.debug_current_window_safe()   #현재창 확인용 메서드
                    time.sleep(2)
                    self.driver.close()
                    time.sleep(2)
                    print("팝업 창 종료")
                    break
            if len(self.driver.window_handles) < 3 : 
                break
        
        self.driver.switch_to.window(original_account_window) 
        return True        

    #항목 별 저장 시 토스트 팝업 문구 비교 메서드
        
    def toast_save_msg_compare(self):
        #toast 문구 확인
        toast_containers = self.get_elements(By.XPATH,XPATH["TOAST_CONTAINER"],option="visibility", timeout=5 )
        for toast_container in toast_containers:
            toast_msg = toast_container.text
            time.sleep(1)
            print(f"{toast_msg}")
            return True
    
    def click_to_promotion(self):
        element = self.get_element_by_name(NAME["BTN_MKT"])
        element.click()
        time.sleep(4)
        return True