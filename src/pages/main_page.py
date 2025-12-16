from utils.headers import *

from pages.base_page import BasePage
from utils.defines import SELECTORS, XPATH, TARGET_URL, TIMEOUT_MAX

from enums.ui_status import MenuStatus


from controllers.chat_input_controller import ChatInputController
from controllers.clipboard_controller import ClipboardController
from controllers.response_controller import ResponseController
from controllers.scroll_controller import ScrollController

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  
        self.menu_status = MenuStatus.OPENED

    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])

    # ================= main 공용 ===================== #
    def click_btn_by_xpath(self, xpath, option):
        btn = self.get_element_by_xpath(xpath, option)
        if btn and btn.is_enabled():
            btn.click()
            time.sleep(0.5)
            return True
        return False
        
    # ================================================ #        
    def click_btn_home_menu(self, button_text: str):
        try:
            buttons = self.get_elements_by_css_selector(SELECTORS["BTNS_HOME_MENU"])

            for btn in buttons:
                if btn.text.strip() == button_text:
                    btn.click()
                    return True  
            return False
        
        except NoSuchElementException:
            return False
        
    # ================ 추후 past_chat_page로 뺄 예정 ================ 
    def click_on_past_chat(self):
        try:
            items = self.get_elements_by_css_selector(SELECTORS["CHAT_LIST_ITEMS"])
            if not items:
                raise Exception("대화 내역이 없습니다.")

            latest = min(items, key=lambda x: int(x.get_attribute("data-item-index")))
            latest.click()
            time.sleep(1)
            return False
        
        except NoSuchElementException:
            return False
        
    # ================  Scroll ================ 
    def scroll_up_chat(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_MAIN_CHAT"])
        return ScrollController.scroll_up(self.driver, area)

    def scroll_down_chat(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_MAIN_CHAT"])
        return ScrollController.scroll_down(self.driver, area)

    def click_btn_scroll_to_bottom(self, timeout = TIMEOUT_MAX):
        start = time.time()

        while time.time() - start < timeout:
            btn = self.get_element_by_css_selector(SELECTORS["BTN_SCROLL_TO_BOTTOM"])
            if btn and btn.is_enabled():
                try:
                    btn.click()
                    time.sleep(3)
                    return True
                except Exception:
                    pass

            self.scroll_up_chat()

    # ================  Chat ================ 
    def action_user_chat(self, chat_key ,chat_type):
        ai_input_lst = self.fm.read_json_file("ai_text_data.json")[chat_key]   
        for item in ai_input_lst:
            if item["type"] != chat_type:
                continue   
            self.input_chat(item["content"])  
    
    def click_send(self):
        self.click_btn_by_xpath(XPATH["BTN_SEND"], option = "presence")
        time.sleep(0.5)

    def input_chat(self, text: str):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.send_text(textarea, text)
        self.click_send()
    
        ResponseController.wait_for_resp(btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]))
    
    def click_btn_retry(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_RETRY"])
        if not btns:
            raise Exception("다시 생성하기 버튼이 없음.")
        btns[-1].click()

        ResponseController.wait_for_resp(btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]))
        time.sleep(1)

    # ================ Clipboard ================ 
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
        ChatInputController.paste_text(textarea, self.copy_last_response())
        time.sleep(0.5)
    
    def reset_chat(self):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.reset_text(textarea)
        time.sleep(0.5)

    # ================  메뉴 ================ 
    def sync_menu_status(self):
        try:
            # 메뉴 열기 버튼이 보이면 CLOSED 상태
            btn_open = self.get_element_by_xpath(XPATH["BTN_MENU_OPEN"])
            if btn_open and btn_open.is_displayed():
                self.menu_status = MenuStatus.CLOSED
                return
        except NoSuchElementException:
            pass

        try:
            # 메뉴 닫기 버튼이 보이면 OPENED 상태
            btn_close = self.get_element_by_xpath(XPATH["BTN_MENU_CLOSE"])
            if btn_close and btn_close.is_displayed():
                self.menu_status = MenuStatus.OPENED   
        except NoSuchElementException:
            pass
        
    def toggle_menu(self, btn_element):
        if not btn_element:
            print("버튼 찾기 실패")
            return

        if btn_element.is_enabled():
            btn_element.click()
            time.sleep(0.5)
            
            if self.menu_status == MenuStatus.CLOSED:
                self.menu_status = MenuStatus.OPENED  
            else:
                self.menu_status = MenuStatus.CLOSED
            print(self.menu_status)

    def action_menu_arrow(self):
        if self.menu_status == MenuStatus.CLOSED: 
            btn_arrow = self.get_element_by_xpath(XPATH["BTN_MENU_OPEN"])
        else: 
            btn_arrow = self.get_element_by_xpath(XPATH["BTN_MENU_CLOSE"])
        self.toggle_menu(btn_arrow)

    def action_menu_bar(self):
        btn_bar = self.get_element_by_css_selector(SELECTORS["BTN_MENU_BAR"])
        self.toggle_menu(btn_bar)
    
    #================ 파일 업로드 ================ 
    def open_upload_file_dialog(self):
        plus = self.get_element_by_css_selector(SELECTORS["BTN_UPLOAD_PLUS_CSS"])
        if plus and plus.is_enabled():
            plus.click()
            time.sleep(0.5)

    def paste_file_path_and_send(self, file_path):   
        ClipboardController.copy(file_path)
        ClipboardController.paste_file_path()
        self.click_send()
        ResponseController.wait_for_resp(btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]))

    def action_upload_file(self, file_path):
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_UPLOAD_FILE"], option = "visibility")
        self.paste_file_path_and_send(file_path)
        
    def upload_files(self):
        images = self.fm.get_asset_files((".jpg", ".png"))
        for img in images:
            self.action_upload_file(file_path = img)
            
        allowed_files = self.fm.get_asset_files((".md", ".pdf", ".csv"))
        for file in allowed_files:
            self.action_upload_file(file_path = file)
        
        not_allowed_files = self.fm.get_asset_files((".psd", ".exe", ".zip"))
        for file in not_allowed_files:
            self.action_upload_file(file_path = file)
        
    # ================ 이미지 생성 ================ 
    def action_gen_image(self):
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_GEN_IMAGE"], option = "visibility")
        
        

    # ================ 웹 검색 ================== 
    def action_search_web(self):
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_SEARCH_WEB"], option = "visibility")
        