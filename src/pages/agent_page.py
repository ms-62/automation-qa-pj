from utils.headers import *
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage
from managers.file_manager import FileManager
from utils.defines import TARGET_URL, SELECTORS, NAME, XPATH
from utils.defines import TIMEOUT_MAX

from enums.ui_status import MenuStatus
from selenium.webdriver.common.action_chains import ActionChains
from controllers.chat_input_controller import ChatInputController
from controllers.clipboard_controller import ClipboardController
from controllers.response_controller import ResponseController
from controllers.scroll_controller import ScrollController

class AgentPage(BasePage) :
    def __init__(self, driver):
        super().__init__(driver)
        self.fm = FileManager()
        
    def go_to_agent_page(self):
        menu_btn = self.get_element_by_xpath(XPATH["AGENT_MENU_BTN"])
        menu_btn.click()
       
#========================= 에이전트 검색 ================================================================================

    def search_input(self, agents) :
        search = self.get_element_by_xpath(
            XPATH["AGENT_SEARCH"],
            option="visibility",
            timeout=10
        )
        search.click()
        search.clear()
        search.send_keys(agents)
        
    def search_result(self) :
        result = self.get_element_by_xpath(XPATH["AGENT_SEARCH_RESULT"])
        return result
    
    def search_no_result(self) :
        result = self.get_element_by_xpath(XPATH["AGENT_SEARCH_NO_RESULT"])
        return result
    
#============================= 에이전트 대화로 만들기 ==========================================================================
        
    # 에이전트 만들기 창 들어가기
    def make_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["GO_MAKE_AGENT"])
        element.click()
    
    # 대화로 만들기 메뉴 버튼 클릭
    def go_to_make_chat(self) :
        self.get_element_by_xpath(XPATH["GO_TO_MAKE_CHAT"]).click()
        
    # 대화로 만들기 창 찾기
    def get_chat_area(self):
        return self.get_element_by_xpath(
            "//div[contains(@class,'css-1r7pci0')]//div[contains(@class, 'css-ogm1eb')]",
            option="presence",
            timeout=5
        )
        
    # 대화로 만들기 응답 부분 추출
    def get_chatmake_ai_response_area(self) :
        chat_area = self.get_chat_area()
        try :
            return chat_area.find_element(By.CSS_SELECTOR, 'div[data-status="complete"]')
        except :
            return None
    
    # 대화로 만들기 응답 완료
    def chatmake_input_chat(self, text: str, timeout=20) :
        chat_area = self.get_chat_area()
        textarea = chat_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ChatInputController.send_text(textarea, text)
        send_btn = chat_area.find_element(By.XPATH, ".//button[@aria-label='보내기']")
        if send_btn.is_enabled():
            send_btn.click()
        else:
            raise Exception("미리보기 전송 버튼이 활성화되지 않았습니다!")
        
        result = ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_chatmake_ai_response_area,
            timeout=timeout
        )
        return result
        
    # 대화로 만들기 응답 중지
    def chatmake_input_chat_stop(self, text: str):
        chat_area = self.get_chat_area()
        
        textarea = chat_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ChatInputController.send_text(textarea, text)
        
        send_btn = chat_area.find_element(By.XPATH, ".//button[@aria-label='보내기']")
        if send_btn.is_enabled():
            send_btn.click()
        else:
            raise Exception("미리보기 전송 버튼이 활성화되지 않았습니다!")
    
        result = ResponseController.wait_for_response_with_timeout(
            btn_stop=lambda: chat_area.find_element(By.XPATH, './/button[@aria-label="취소"]'),
            stop_time=1.5
        )
        return result
    
    # 대화로 만들기 다시 생성
    def chatmake_create_again_response(self, timeout=20):
        chat_area = self.get_chat_area()
        btn = WebDriverWait(chat_area, timeout).until(
            lambda area: (
                (btns := area.find_elements(By.XPATH, './/button[@aria-label="다시 생성"]'))
                and btns[-1].is_enabled()
                and btns[-1]
            )
        )
        btn.click()

        WebDriverWait(chat_area, timeout).until(
            lambda area: (
                elems := area.find_elements(By.CSS_SELECTOR, 'div[data-status]')
            ) and elems[-1].get_attribute("data-status") == "running"
        )

        WebDriverWait(chat_area, timeout).until(
            lambda area: (
                elems := area.find_elements(By.CSS_SELECTOR, 'div[data-status]')
            ) and elems[-1].get_attribute("data-status") == "complete"
        )
        return True
    
    def check_chatmake_create_again_response(self) :
        chat_area = self.get_chat_area()
        element = chat_area.find_element(By.XPATH, ".//p[contains(@class, 'css-3uvjx')]")
        return element
    
    # 대화로 만들기 응답 부분 복사
    def copy_last_response_in_chatmake(self, timeout=20) :
        chat_area = self.get_chat_area()
        btn = WebDriverWait(chat_area, timeout).until(
            lambda area: (
                (btns := area.find_elements(By.XPATH, './/button[@aria-label="복사"]'))
                and btns[-1].is_displayed()
                and btns[-1].is_enabled()
                and btns[-1]
            )
        )

        btn.click()
        print("복사 완성")
        return ClipboardController.read()
    
    def paste_last_response_in_chatmake(self):
        chat_area = self.get_chat_area()
        textarea = chat_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ClipboardController.paste(textarea)   # 클립보드에서만 붙여넣기
        time.sleep(0.5)
        
    def check_paste_in_chatmake(self) :
        chat_area = self.get_chat_area()
        text = chat_area.find_element(By.CSS_SELECTOR, "textarea[name='input']").text.strip()
        return text
    
#========================= 에이전트 설정으로 만들기 ===========================================================================
        
    # 설정 메뉴 입력
    def setting_name_input(self, text: str) :
        namearea = self.get_element_by_xpath(XPATH["NAME_SETT"])
        ChatInputController.send_text(namearea, text)
        
    def setting_intro_input(self, text: str) :
        introarea = self.get_element_by_xpath(XPATH["INTRO_SETT"])
        ChatInputController.send_text(introarea, text)
        
    def setting_rule_input(self, text: str) :
        rulearea = self.get_element_by_xpath(XPATH["RULE_SETT"])
        ChatInputController.send_text(rulearea, text)
        
    def setting_card_input(self, text: str) :
        cardarea = self.get_element_by_xpath(XPATH["CARD_SETT"])
        ChatInputController.send_text(cardarea, text)
        
    def make_agent_for_me(self) :
        element = self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"], option="clickable")
        element.click()
        me = self.get_element_by_xpath(XPATH["BTN_FOR_ME"])
        me.click()
        btn = self.get_element_by_xpath(XPATH["BTN_AGENT_PUBLISH"])
        btn.click()
        check = self.get_element_by_xpath(XPATH["CHECK_MAKE"])
        return check
        
    def make_agent_for_agency(self) :
        element = self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"], option="clickable")
        element.click()
        agency = self.get_element_by_xpath(XPATH["BTN_FOR_AGENCY"])
        agency.click()
        btn = self.get_element_by_xpath(XPATH["BTN_AGENT_PUBLISH"])
        btn.click()
        check = self.get_element_by_xpath(XPATH["CHECK_MAKE"])
        return check
        
    def check_btn_disabled(self) :
        element = self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"])
        return element
    
    def error_message(self) :
        element = self.get_element_by_xpath(XPATH["ERROR_MSG"], timeout=3)
        return element
    
    def delete_card(self) :
        elements = self.get_elements_by_xpath(XPATH["DELETE_CARD"])
        element = elements[1]
        element.click()
        
    def check_card_number(self) :
        elements = self.get_elements_by_xpath(XPATH["DELETE_CARD"])
        return elements
    
    def multi_function(self) :
        elements = self.get_elements_by_xpath(
        XPATH["SELECT_FUNCTION"],
        option="clickable"
    )
        for element in elements :
            if not element.is_selected():
                element.click()
                
#======================= 에이전트 설정으로 만들기 - 이미지 ==============================================
                
    # 이미지 업로드    
    def upload_image(self, file_name: str):
        file_input = self.get_element_by_css_selector(
            SELECTORS["IMAGE_FILE_INPUT"]
        )
        file_path = self.fm.get_asset_path(file_name)
        file_input.send_keys(file_path)
        
    # 이미지 업로드 체크
    def check_upload_image(self, timeout) :
        uploaded = self.get_element_by_xpath(XPATH["UPLOADED_IMAGE_PREVIEW"], timeout=timeout)
        return uploaded
    
    def check_upload_big_img(self) :
        img = self.get_element_by_xpath(XPATH["UPLOADED_IMAGE_PREVIEW"])
        src = img.get_attribute("src")
        return src is not None and src.strip() != ""
    
    # 이미지 생성기
    def make_image(self) :
        self.get_element_by_xpath(XPATH["BTN_ADD_IMAGE"]).click()
        btns = self.get_elements_by_xpath(XPATH["BTN_MAKE_IMAGE"])
        btn = btns[1]
        btn.click()
        
#======================= 에이전트 설정으로 만들기 - 파일 ==============================================
        
    # 파일 업로드
    def upload_file(self, file_name: str) :
        file_input = self.get_element_by_css_selector(
            SELECTORS["FILE_INPUT"]
        )
        file_path = self.fm.get_asset_path(file_name)
        file_input.send_keys(file_path)
        
    # 다중 파일 업로드
    def upload_multiple_images(self, extensions=(".pdf"), limit=None):
        file_input = self.get_element_by_css_selector(
            SELECTORS["FILE_INPUT"]
        )

        file_paths = self.fm.get_asset_files(extensions)

        if limit:
            file_paths = file_paths[:limit]

        file_input.send_keys("\n".join(file_paths))
        
    # 파일 업로드 체크
    def check_upload_file(self) :
        uploaded = self.get_element_by_xpath(XPATH["CHECK_UPLOADED_FILE"], timeout=3)
        return uploaded
    
    def check_fail_file_upload(self) :
        uploaded = self.get_element_by_xpath(XPATH["FAIL_UPLOAD_FILE"])
        return uploaded
    
    def check_fail_msg_file_upload(self) :
        msg = self.get_element_by_xpath(XPATH["FAIL_UPLOAD_FILE_MSG"])
        return msg
    
    # 파일 삭제
    def delete_for_uploaded_file(self) :
        btns = self.get_elements_by_xpath(XPATH["BTN_FOR_UPLOADED_FILE"])
        btn = btns[1]
        btn.click()
        
#========================== 에이전트 만들기 - 스크롤 ============================================================
        
    # 설정 스크롤
    def scroll_down_setting(self) :
        area = self.get_elements_by_xpath(XPATH["SCROLL_MAKE_AGENT"])
        ScrollController.scroll_down(self.driver, area[0])
        
#========================== 에이전트 만들기 - 뒤로가기 관련 ============================================================
    
    # 에이전트 만들기 뒤로가기 버튼
    def back_in_agent_make_screen(self) :
        btn = self.get_element_by_xpath(XPATH["BTN_BACK_IN_MAKE_AGENT"])
        btn.click()
        
    # 내 에이전트 창 이동
    def go_to_my_agent(self) :
        element = self.get_element_by_xpath(XPATH["MY_AGENT_BTN"])
        element.click()
        time.sleep(1)
        
    # 초안 메시지 확인
    def check_draft_msg(self) :
        msg = self.get_element_by_xpath(XPATH["CHECK_DRAFT"], option="visibility")
        return msg
    
#=================== 에이전트 만들기 - 미리보기 ==========================================================
        
    # 미리보기 대화창 찾기
    def get_preview_area(self):
        return self.get_element_by_xpath(
            "//div[contains(@class,'css-1r7pci0')]//div[contains(@class,'css-ml5yxu')]",
            option="presence",
            timeout=5
        )
        
    # 에이전트 미리보기 대화 카드 클릭
    def preview_agent_talk_card_click(self) :
        preview_area = self.get_preview_area()
        element = preview_area.find_element(By.XPATH, "//button[contains(@class, 'uy7nb7')]")
        element.click()
    
    # 에이전트 대화창 - 질문 내용 받기
    def preview_check_my_talk_input(self) :
        preview_area = self.get_preview_area()
        text = preview_area.find_element(By.XPATH, "//span[@data-status = 'complete']")
        return text
    
    # 미리보기 대화창 응답 부분 추출
    def get_preview_ai_response_area(self) :
        preview_area = self.get_preview_area()
        try :
            return preview_area.find_element(By.CSS_SELECTOR, 'div[data-status="complete"]')
        except :
            return None
    
    # 에이전트 미리보기 대화창 응답 완료
    def preview_input_chat(self, text: str, timeout=20) :
        preview_area = self.get_preview_area()
        textarea = preview_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ChatInputController.send_text(textarea, text)
        send_btn = preview_area.find_element(By.XPATH, ".//button[@aria-label='보내기']")
        if send_btn.is_enabled():
            send_btn.click()
        else:
            raise Exception("미리보기 전송 버튼이 활성화되지 않았습니다!")
        
        result = ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_preview_ai_response_area,
            timeout=timeout
        )
        return result
        
    # 에이전트 미리보기 대화창 응답 중지
    def preview_input_chat_stop(self, text: str):
        preview_area = self.get_preview_area()
        
        textarea = preview_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ChatInputController.send_text(textarea, text)
        
        send_btn = preview_area.find_element(By.XPATH, ".//button[@aria-label='보내기']")
        if send_btn.is_enabled():
            send_btn.click()
        else:
            raise Exception("미리보기 전송 버튼이 활성화되지 않았습니다!")
    
        result = ResponseController.wait_for_response_with_timeout(
            btn_stop=lambda: preview_area.find_element(By.XPATH, '//button[@aria-label="취소"]'),
            stop_time=3
        )
        return result
    
    # 에이전트 미리보기 다시 생성
    def preview_create_again_response(self, timeout=20):
        preview_area = self.get_preview_area()

        btn = WebDriverWait(preview_area, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, './/button[@aria-label="다시 생성"]')
            )
        )
        btn.click()

        return ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_preview_ai_response_area,
            timeout=timeout
        )
    
    def check_preview_create_again_response(self) :
        preview_area = self.get_preview_area()
        element = preview_area.find_element(By.XPATH, ".//p[contains(@class, 'css-3uvjx')]")
        return element
        
    # 에이전트 미리보기 새로고침
    def refresh_btn_in_preview(self) :
        element = self.get_element_by_xpath(XPATH["BTN_PREVIEW_REFRESH"])
        element.click()
        
    # 미리보기 새로고침 확인
    def check_refresh_in_preview(self) :
        preview_area = self.get_preview_area()
        element = WebDriverWait(self.driver, 3).until(
            lambda d: preview_area.find_element(
                By.XPATH, ".//div[contains(@class, 'css-j7q6vj')]"
            )
        )
        return element
    
    # 미리보기 응답 부분 복사
    def copy_last_response_in_preview(self) :
        preview_area = self.get_preview_area()
        btns = preview_area.find_elements(By.XPATH, '//button[@aria-label="복사"]')
        if not btns:
            raise Exception("복사 버튼이 없음.")

        btns[-1].click()
        time.sleep(0.5)
        print("복사 완성")
        return ClipboardController.read()
    
    def paste_last_response_in_preview(self):
        preview_area = self.get_preview_area()
        textarea = preview_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ClipboardController.paste(textarea)   # 클립보드에서만 붙여넣기
        time.sleep(0.5)
        
    def check_paste_in_preview(self) :
        preview_area = self.get_preview_area()
        text = preview_area.find_element(By.CSS_SELECTOR, "textarea[name='input']").text.strip()
        return text
        
#====================== 에이전트와 대화 ============================================================
        
    # 스크롤
    def scroll_up_chat(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_MAIN_CHAT"])
        ScrollController.scroll_up(self.driver, area)
    
    # 에이전트 대화창 들어가기
    def talk_with_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK"])
        element.click()
    
    # 대화 카드 관련
    def agent_talk_card_text(self):
        element_text = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD_TEXT"])
        return element_text
        
    def agent_talk_card_click(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD"])
        element.click()
    
    # 질문 내용 받기
    def check_my_talk_input(self) :
        text = self.get_element_by_xpath(XPATH["AGENT_INPUT_TEXT"])
        return text
    
    # 보내기 버튼
    def click_send(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SEND"])
        if btn.is_enabled():
            btn.click()
    
    # 에이전트가 응답하는 부분
    def get_ai_response_area(self) :
        try :
            return self.get_element_by_css_selector(SELECTORS["CHECK_CHAT_COMPLETE"])
        except :
            return None
    
    # 응답 완료 상황  
    def ai_chat_complete(self, text: str, timeout=20) :
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
        
        result = ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_ai_response_area,
            timeout=timeout
        )
        return result
    
    # 중단 버튼 상황
    def input_chat_stop(self, text: str):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
    
        result = ResponseController.wait_for_response_with_timeout(
            btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]),
            stop_time=3
        )
        return result
    
    # 다시 생성 버튼
    def create_again_response(self, timeout=20) :
        self.get_element_by_xpath(XPATH["BTN_RETRY"]).click()
        result = ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_ai_response_area,
            timeout=timeout
        )
        return result
    
    def check_create_again_response(self) :
        element = self.get_element_by_xpath(XPATH["CHECK_CREATE_AGAIN_RESPONSE"])
        return element
    
    # AI 응답 내용 복사
    def copy_last_response(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_COPY_RESPONE"])
        if not btns:
            raise Exception("복사 버튼이 없음.")

        btns[-1].click()
        time.sleep(0.5)
        print("복사 완성")
        return ClipboardController.read()
    
    def paste_last_response(self):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ClipboardController.paste(textarea)   # 클립보드에서만 붙여넣기
        time.sleep(0.5)
        
    def check_paste(self) :
        text = self.get_element_by_css_selector(SELECTORS["TEXTAREA"]).text.strip()
        return text

#========================= 대화창 파일 관련=================================================================================
        
    # 브라우저 파일 선택창 열기
    def open_upload_file_dialog(self):
        plus = self.get_element_by_css_selector(SELECTORS["BTN_UPLOAD_PLUS_CSS"])
        if plus and plus.is_enabled():
            plus.click()
            time.sleep(0.5)
        btn = self.get_element_by_xpath(XPATH["BTN_UPLOAD_FILE"], option = "visibility")
        if btn and btn.is_enabled() :
            btn.click()
            time.sleep(2)

    # 단일 파일 업로드
    def upload_file_in_chat(self) :
        file_path = self.fm.get_asset_path("test_pdf.pdf")
        ClipboardController.paste_file_path(file_path)
        
    def check_file_upload_in_chat(self) :
        element = self.get_element_by_xpath(XPATH["CHECK_FILE_IN_CHAT"], timeout=3)
        return element
    
    # 단일 사진 업로드
    def upload_img_in_chat(self) :
        file_path = self.fm.get_asset_path("test_asset.jpg")
        ClipboardController.paste_file_path(file_path)
        
    def check_img_upload_in_chat(self) :
        element = self.get_element_by_xpath(XPATH["CHECK_IMG_IN_CHAT"])
        return element
    
    # 사진 옵션
    def download_img_in_chat(self) :
        area = self.get_element_by_xpath(XPATH["IMG_AREA"])

        ActionChains(self.driver) \
            .move_to_element(area) \
            .pause(0.3) \
            .perform()

        btns = self.get_elements_by_xpath(XPATH["IMG_BTNS"])
        btn = btns[1]
        btn.click()

        return True
    
    def expand_img_in_chat(self) :
        area = self.get_element_by_xpath(XPATH["IMG_AREA"])

        ActionChains(self.driver) \
            .move_to_element(area) \
            .pause(0.3) \
            .perform()

        btns = self.get_elements_by_xpath(XPATH["IMG_BTNS"])
        btn = btns[2]
        btn.click()

        return True
    
    def downsize_img_in_chat(self) :
        btn = self.get_element_by_xpath(XPATH["DOWNSIZE_BTN"])
        btn.click()
        time.sleep(1)
        element = self.get_element_by_xpath(XPATH["DOWNSIZE_BTN"], timeout=3)
        return element
        
    
    # 파일 옵션 
    def delete_file_in_chat(self) :
        self.get_element_by_xpath(XPATH["DELETE_FILE"]).click()
    
    # 용량 큰 단일 파일
    def upload_big_file_in_chat(self) :
        file_path = self.fm.get_asset_path("big_file.md")
        ClipboardController.paste_file_path(file_path)
        
    def wait_until_loading_disappear(self) :
        element = self.get_element_by_xpath(XPATH["LOADING_ICON"])
        WebDriverWait(self, 30).until(
        EC.staleness_of(element)
    )
        return True
    
    # 실행 파일 업로드
    def upload_exe_file_in_chat(self) :
        file_path = self.fm.get_asset_path("test_exe.exe")
        ClipboardController.paste_file_path(file_path)
        
    # 여러 파일 업로드
    def upload_files_in_chat(self) :   
        file_paths = self.fm.get_asset_files((".pdf",))
        for file_path in file_paths :
            self.open_upload_file_dialog()
            time.sleep(0.5)
            ClipboardController.paste_file_path(file_path)
            
# ====================== 에이전트 수정 & 삭제 ===================================

    # 에이전트 수정
    def go_to_modify_in_agents(self) :
        element = self.get_element_by_xpath(XPATH["DOT_IN_AGENTS"])
        if element and element.is_enabled():
            element.click()
            time.sleep(0.5)
        btns = self.get_elements_by_xpath(XPATH["MODIFY_AND_DELETE_IN_DOT"])
        if btns :
            btns[0].click()
            time.sleep(0.5)
        
    def go_to_modify_in_my_agent(self) :
        btns = self.get_elements_by_xpath(XPATH["BTNS_IN_MY_AGENT"])
        btns[0].click()
        time.sleep(0.5)
            
    def modify_name(self, text: str) :
        namearea = self.get_element_by_xpath(XPATH["NAME_SETT"])
        ChatInputController.reset_text(namearea)
        ChatInputController.send_text(namearea, text)
        
    def modify_intro(self, text: str) :
        introarea = self.get_element_by_xpath(XPATH["INTRO_SETT"])
        ChatInputController.reset_text(introarea)
        ChatInputController.send_text(introarea, text)
        
    def modify_rule(self, text: str) :
        rulearea = self.get_element_by_xpath(XPATH["RULE_SETT"])
        ChatInputController.reset_text(rulearea)
        ChatInputController.send_text(rulearea, text)
        
    def modify_card(self, text: str) :
        cardarea = self.get_element_by_xpath(XPATH["CARD_SETT"])
        ChatInputController.reset_text(cardarea)
        ChatInputController.send_text(cardarea, text)
    
    def modify_and_check(self) :
        self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"], option="clickable").click()
        time.sleep(0.5)
        self.get_element_by_xpath(XPATH["BTN_AGENT_PUBLISH"]).click()
        element = self.get_element_by_css_selector(SELECTORS["UPDATE_CHECK"], timeout=5)
        return element
        
# =========================== 에이전트 삭제 ===================================================================

    def check_delete_in_agents(self) :
        element = self.get_element_by_xpath(XPATH["DELETE_CHECK"], timeout=5)
        return element
        
    def go_to_delete_in_agents(self) :
        element = self.get_element_by_xpath(XPATH["DOT_IN_AGENTS"])
        if element and element.is_enabled():
            element.click()
            time.sleep(0.5)
        btns = self.get_elements_by_xpath(XPATH["MODIFY_AND_DELETE_IN_DOT"])
        if btns :
            btns[1].click()
            time.sleep(0.5)
        options = self.get_elements_by_xpath(XPATH["DELETE_OPTIONS_IN_AGENTS"])
        if options :
            options[1].click()
        
    def go_to_not_delete_in_agents(self) :
        element = self.get_element_by_xpath(XPATH["DOT_IN_AGENTS"])
        if element and element.is_enabled():
            element.click()
            time.sleep(0.5)
        btns = self.get_elements_by_xpath(XPATH["MODIFY_AND_DELETE_IN_DOT"])
        if btns :
            btns[1].click()
            time.sleep(0.5)
            options = self.get_elements_by_xpath(XPATH["DELETE_OPTIONS_IN_AGENTS"])
        if options :
            options[0].click()
            
    def check_delete_in_my_agent(self) :
        element = self.get_element_by_xpath(XPATH["DELETE_CHECK"], timeout=5)
        return element
        
    def go_to_delete_in_my_agent(self) :
        btns = self.get_elements_by_xpath(XPATH["BTNS_IN_MY_AGENT"])
        btns[1].click()
        time.sleep(0.5)
        btns = self.get_elements_by_xpath(XPATH["DELETE_OPTIONS_IN_MY_AGENT"])
        if btns :
            btns[1].click()
        
    def go_to_not_delete_in_my_agent(self) :
        btns = self.get_elements_by_xpath(XPATH["BTNS_IN_MY_AGENT"])
        btns[1].click()
        time.sleep(0.5)
        btns = self.get_elements_by_xpath(XPATH["DELETE_OPTIONS_IN_MY_AGENT"])
        if btns :
            btns[0].click()