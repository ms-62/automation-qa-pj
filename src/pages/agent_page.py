from utils.headers import *

from pages.base_page import BasePage
from managers.file_manager import FileManager
from utils.defines import TARGET_URL, SELECTORS, NAME, XPATH
from utils.defines import TIMEOUT_MAX

from enums.ui_status import MenuStatus

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
        self.get_element_by_xpath(
            XPATH["MY_AGENT_BTN"],
            option="clickable",
            timeout=10
        )
       
    # 에이전트 탐색창 - 검색 기능 
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
    
#===========================에이전트 만들기 관련==================================
        
    # 에이전트 만들기 창 들어가기
    def make_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["GO_MAKE_AGENT"])
        element.click()
        
    # 설정 메뉴 관련
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
        element = self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"])
        element.click()
        me = self.get_element_by_xpath(XPATH["BTN_FOR_ME"])
        me.click()
        btn = self.get_element_by_xpath(XPATH["BTN_AGENT_PUBLISH"])
        btn.click()
        time.sleep(3)
        check = self.get_element_by_xpath(XPATH["CHECK_MAKE"])
        return check
        
    def make_agent_for_agency(self) :
        element = self.get_element_by_xpath(XPATH["BTN_AGENT_MAKE"])
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
        element = self.get_element_by_xpath(XPATH["ERROR_MSG"])
        return element
    
    def delete_card(self) :
        element = self.get_element_by_xpath(XPATH["DELETE_CARD"])
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
                time.sleep(0.2)
                
    # 에이전트 만들기 - 이미지 업로드    
    def upload_image(self, file_name: str):
        file_input = self.get_element_by_css_selector(
            SELECTORS["IMAGE_FILE_INPUT"]
        )
        file_path = self.fm.get_asset_path(file_name)
        file_input.send_keys(file_path)
        
    # 이미지 업로드 체크
    def check_upload_image(self) :
        uploaded = self.get_element_by_xpath(XPATH["UPLOADED_IMAGE_PREVIEW"])
        return uploaded
    
    def check_upload_big_img(self) :
        img = self.get_element_by_xpath(XPATH["UPLOADED_IMAGE_PREVIEW"])
        src = img.get_attribute("src")
        return src is not None and src.strip() != ""
    
    # 에이전트 만들기 - 이미지 생성기
    def make_image(self) :
        self.get_element_by_xpath(XPATH["BTN_ADD_IMAGE"]).click()
        btns = self.get_elements_by_xpath(XPATH["BTN_MAKE_IMAGE"])
        btn = btns[1]
        btn.click()
        
    # 에이전트 만들기 - 파일 업로드
    def upload_file(self, file_name: str) :
        file_input = self.get_element_by_css_selector(
            SELECTORS["FILE_INPUT"]
        )
        file_path = self.fm.get_asset_path(file_name)
        file_input.send_keys(file_path)
        
    # 에이전트 만들기 - 다중 파일 업로드
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
        uploaded = self.get_element_by_xpath(XPATH["CHECK_UPLOADED_FILE"])
        return uploaded
    
    def check_fail_file_upload(self) :
        uploaded = self.get_element_by_xpath(XPATH["FAIL_UPLOAD_FILE"])
        return uploaded
    
    def check_fail_msg_file_upload(self) :
        msg = self.get_element_by_xpath(XPATH["FAIL_UPLOAD_FILE_MSG"])
        return msg
    
    # 파일 삭제 for uploaded file
    def delete_for_uploaded_file(self) :
        btns = self.get_elements_by_xpath(XPATH["BTN_FOR_UPLOADED_FILE"])
        btn = btns[1]
        btn.click()
    
    # 에이전트 만들기 뒤로가기 버튼
    def back_in_agent_make_screen(self) :
        btns = self.get_elements_by_xpath(XPATH["BTN_BACK_IN_MAKE_AGENT"])
        btn = btns[1]
        btn.click()
                
    # 에이전트 만들기 - 설정 스크롤
    def scroll_down_setting(self) :
        area = self.get_elements_by_xpath(XPATH["SCROLL_MAKE_AGENT"])
        ScrollController.scroll_down(self.driver, area[0])
        
    # 내 에이전트 창 이동
    def go_to_my_agent(self) :
        element = self.get_element_by_xpath(XPATH["MY_AGENT_BTN"])
        element.click()
        
    # 초안 메시지 확인
    def check_draft_msg(self) :
        msg = self.get_element_by_xpath(XPATH["CHECK_DRAFT"])
        return msg
        
    # 에이전트 미리보기 대화창(중단)
    def preview_input_chat_stop(self, text: str):
        # 1. 전체 영역 안에서 미리보기 영역 찾기
        preview_area = self.get_element_by_xpath(
            "//div[contains(@class,'css-1r7pci0')]//div[contains(@class,'css-ml5yxu')]",
            option="presence",  # 존재 여부만 확인
            timeout=5
        )
        
        textarea = preview_area.find_element(By.CSS_SELECTOR, "textarea[name='input']")
        ChatInputController.send_text(textarea, text)
        
        send_btn = preview_area.find_element(By.XPATH, ".//button[@aria-label='보내기']")
        if send_btn.is_enabled():
            send_btn.click()
        else:
            raise Exception("미리보기 전송 버튼이 활성화되지 않았습니다!")
    
        result = ResponseController.wait_for_resp(
            btn_stop=lambda: preview_area.find_element(By.XPATH, '//button[@aria-label="취소"]')
        )
        time.sleep(1)
        return result
        
    # 에이전트 미리보기 새로고침
    def refresh_btn_in_preview(self) :
        element = self.get_element_by_xpath(XPATH["BTN_PREVIEW_REFRESH"])
        element.click()
        
#======================대화 관련==============================================
        
    # 에이전트 대화창 - 스크롤
    def scroll_up_chat(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_MAIN_CHAT"])
        ScrollController.scroll_up(self.driver, area)

    def scroll_down_chat(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_MAIN_CHAT"])
        ScrollController.scroll_down(self.driver, area)
        
    def click_btn_scroll_to_bottom(self, timeout = TIMEOUT_MAX, wait_time=3):
        start = time.time()

        while time.time() - start < timeout:
            btn = self.get_element_by_css_selector(SELECTORS["SCROLL_TO_BOTTOM_BUTTON"])

            if btn and btn.is_enabled():
                try:
                    btn.click()
                    print("맨 밑으로 이동스크롤 클릭")
                    return True
                except Exception:
                    pass

            self.scroll_up_chat()
            time.sleep(0.3)

        raise TimeoutError("스크롤 버튼 안보임")
    
    # 에이전트 대화창 들어가기
    def talk_with_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK"])
        element.click()
    
    # 에이전트 대화창 대화 카드 관련
    def agent_talk_card_text(self):
        element_text = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD_TEXT"])
        return element_text
        
    def agent_talk_card_click(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD"])
        element.click()
    
    # 에이전트 대화창 - 질문 내용 받기
    def check_my_talk_input(self) :
        text = self.get_element_by_xpath(XPATH["AGENT_INPUT_TEXT"])
        return text
    
    # 에이전트 대화창 보내기 버튼
    def click_send(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SEND"])
        if btn.is_enabled():
            btn.click()
    
    # 에이전트 대화창 (응답 완료 상황)
    def get_ai_response_area(self) :
        try :
            return self.get_element_by_css_selector(SELECTORS["CHECK_CHAT_COMPLETE"])
        except :
            return None
        
    def ai_chat_complete(self, text: str, timeout=20) :
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
        
        result = ResponseController.wait_for_complete(
            ai_response_area_getter=self.get_ai_response_area,
            timeout=timeout
        )
        return result
    
    # 에이전트 대화창 (중단 버튼 상황)
    def input_chat_stop(self, text: str):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
    
        result = ResponseController.wait_for_resp(
            btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"])
        )
        time.sleep(1)
        return result
    
    # 에이전트 대화창 파일 업로드
    def open_upload_file_dialog(self):
        plus = self.get_element_by_css_selector(SELECTORS["BTN_UPLOAD_PLUS_CSS"])
        if plus and plus.is_enabled():
            plus.click()
            time.sleep(0.5)
        btn = self.get_element_by_xpath(XPATH["BTN_UPLOAD_FILE"], option = "visibility")
        if btn and btn.is_enabled() :
            btn.click()
            time.sleep(0.5)

    def upload_file_in_chat(self) :
        file_path = r"D:\elice_python\.myenv\project\ai-heplychat-automation\src\resources\assets\test_pdf.pdf"
        pyautogui.write(file_path)  # 파일 경로 입력
        time.sleep(0.5)
        pyautogui.press('enter')  # 열기 버튼 클릭
        time.sleep(3)
        
    def check_file_upload_in_chat(self) :
        element = self.get_element_by_xpath(XPATH["CHECK_FILE_IN_CHAT"])
        return element
    
    # 에이전트 대화창 사진 업로드
    def upload_img_in_chat(self) :
        file_path = r"D:\elice_python\.myenv\project\ai-heplychat-automation\src\resources\assets\test_asset.jpg"
        pyautogui.write(file_path)  # 파일 경로 입력
        time.sleep(0.5)
        pyautogui.press('enter')  # 열기 버튼 클릭
        time.sleep(3)
        
    def check_img_upload_in_chat(self) :
        element = self.get_element_by_xpath(XPATH["CHECK_IMG_IN_CHAT"])
        return element