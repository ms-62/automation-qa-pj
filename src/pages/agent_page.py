from utils.headers import *

from pages.base_page import BasePage
from utils.defines import TARGET_URL, SELECTORS, NAME, XPATH
from utils.defines import TIMEOUT_MAX

from enums.ui_status import MenuStatus

from controllers.chat_input_controller import ChatInputController
from controllers.clipboard_controller import ClipboardController
from controllers.response_controller import ResponseController
from controllers.scroll_controller import ScrollController

class AgentPage(BasePage) :
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
    
    # 에이전트 대화창 - 나중에 밑에거랑 합치기
    def talk_with_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK"])
        element.click()
        
    def agent_talk_card_text(self):
        element_text = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD_TEXT"])
        return element_text
        
    def agent_talk_card_click(self) :
        element = self.get_element_by_xpath(XPATH["AGENT_TALK_CARD"])
        element.click()
        
    # 에이전트 만들기 - 설정 메뉴 관련
    def make_agent_screen(self) :
        element = self.get_element_by_xpath(XPATH["GO_MAKE_AGENT"])
        element.click()
        
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
        self.fm.file_upload(file_input, file_name)
        
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
                
    # 에이전트 만들기 - 설정 스크롤
    def scroll_down_setting(self) :
        area = self.get_elements_by_xpath(XPATH["SCROLL_MAKE_AGENT"])
        ScrollController.scroll_down(self.driver, area[0])
        
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
    
    # 에이전트 대화창 - 질문 내용 받기
    def check_my_talk_input(self) :
        text = self.get_element_by_xpath(XPATH["AGENT_INPUT_TEXT"])
        return text
    
    # 에이전트 대화창 (중단 버튼)
    def click_send(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SEND"])
        if btn.is_enabled():
            btn.click()

    def input_chat(self, text: str):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
    
        result = ResponseController.wait_for_resp(
            btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"])
        )
        time.sleep(1)
        return result
        
    