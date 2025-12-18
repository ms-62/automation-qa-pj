from utils.headers import *
import re
from pages.base_page import BasePage
from utils.defines import SELECTORS, XPATH, TARGET_URL, TIMEOUT_MAX

from enums.ui_status import MenuStatus, AIresponse
from utils.defines import ChatKey, ChatType
from states.response_state import ResponseState

from controllers.chat_input_controller import ChatInputController
from controllers.clipboard_controller import ClipboardController
from controllers.response_controller import ResponseController
from controllers.scroll_controller import ScrollController

CHAT_TIME = 10
IMAGES_FORMAT = (".jpg", ".png")
ENABLED_FORMAT = (".csv", ".md")
DISABLED_FORMAT = (".psd", ".exe", ".zip")
MUITY_UPLOAD_FORMAT = ".pdf" # 다중 업로드 용으로 만들어놓았음.

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  
        self.menu_status = MenuStatus.NONE
    

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
        
    # ================= home_menu ==================== #        
    def click_btn_home_menu(self, button_text: str):
        try:
            menu = self.get_element_by_xpath(XPATH["BTNS_HOME_MENU"])
            li = menu.find_element(By.XPATH, XPATH["MENU_ITEM_BY_TEXT"].format(text=button_text))
            btn = li.find_element(By.XPATH, XPATH["BTN_EACH_MENU"])
            btn.click()
            return True
        except NoSuchElementException:
            return False
    
    # ---------- 검색 ----------
    def get_search_chat_items(self):
        chat_list = self.get_element_by_xpath(XPATH["SEARCH_CHAT_LIST"])
        time.sleep(1)
        chat_items = chat_list.find_elements(By.XPATH, XPATH["SEARCH_CHAT_ITEMS"])
        return chat_items
        
    def search_past_chats_by_click(self):
        chat_item = self.get_search_chat_items()[0]
        time.sleep(1)
        if chat_item and chat_item.is_enabled():
            self.driver.execute_script("arguments[0].click();", chat_item)

    def search_past_chats_by_input(self):
        input_search = self.get_element_by_xpath(XPATH["INPUT_SEARCH_CHAT"])
        
        chat_items = self.get_search_chat_items()
        for item in chat_items:
            chat_name = item.find_element(By.XPATH, XPATH["SEARCH_CHAT_ITEM_TEXT"]).text.strip()
            if chat_name != "":
                break
            
        ChatInputController.send_text(input_search, chat_name) 
        after_chat_items = self.get_search_chat_items()
        
        if after_chat_items:
            chat_item = after_chat_items[0]
        if chat_item and chat_item.is_enabled():
            self.driver.execute_script("arguments[0].click();", chat_item)
            time.sleep(1)
            return True
        return False                
        
    # ================ past_chat_page ================ #
    def get_selected_chat(self):
        selected_item = self.get_element_by_css_selector(SELECTORS["SELECTED_CHAT"])
        return selected_item

    def get_selected_chat_name(self):
        selected_text = self.get_element_by_css_selector(SELECTORS["SELECTED_CHAT_TEXT"], option="visibility").text.strip()
        return selected_text

    def get_all_chats(self):
        return self.get_elements_by_css_selector(SELECTORS["CHAT_LIST_ITEMS"])

    # ---------- actions ----------
    def open_selected_edit_menu(self):
        selected_chat = self.get_selected_chat()
        self.mouse.move(selected_chat)
        edit_btn = self.get_element_by_css_selector(SELECTORS["BTN_EDIT_PASTCHAT"], option="clickable")
        edit_btn.click()

    def click_change_chat_name(self):
        return self.click_btn_by_xpath(XPATH["BTN_CHANGE_PAST_NAME"], option="presence")

    def click_delete_chat(self):
        return self.click_btn_by_xpath(XPATH["BTN_DELETE_PAST"], option="presence")

    def click_cancel_edit(self):
        return self.click_btn_by_xpath(XPATH["BTN_CANCLE_EDIT"], option="presence")

    def click_save_edit(self):
        return self.click_btn_by_xpath(XPATH["BTN_SAVE_EDIT"], option="clickable")
    
    def click_delete_confirm(self):
        return self.click_btn_by_xpath(XPATH["BTN_DELETE_CONFIRM"], option="clickable")
    
    def select_latest_chat(self):
        items = self.get_all_chats()
        latest = min(items,key=lambda x: int(x.get_attribute("data-item-index")))
        latest.click()
    
    def scroll_up_past_chats(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_PAST_CHATS"])
        return ScrollController.scroll_up(self.driver, area)

    def scroll_down_past_chats(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_PAST_CHATS"])
        return ScrollController.scroll_down(self.driver, area)
    
    # ---------- E2E 용도 ----------
    def rename_chat(self):
        self.open_selected_edit_menu()
        self.click_change_chat_name()
        
        name_area = self.get_element_by_css_selector(SELECTORS["INPUT_CHAT_NAME"])
        ChatInputController.reset_text(name_area)

        prev_name = self.get_selected_chat_name()
        ai_input_lst = self.fm.read_json_file("ai_text_data.json")[ChatKey.RENAME]   
        for item in ai_input_lst:
            content = item["content"]
            if item["type"] != ChatType.CHAT_AI:
                continue  
            if content != prev_name:
                ChatInputController.send_text(name_area, content)    
                break
        self.click_save_edit()
        curname = self.get_selected_chat_name()
        return False if curname == prev_name else True
        
    def delete_chat(self):
        prev_chats = self.get_all_chats()
        self.open_selected_edit_menu()
        self.click_delete_chat()
        self.click_delete_confirm()
        after_chats = self.get_all_chats()
        return False if prev_chats == after_chats else True
        
    def cancel_edit(self):
        self.select_latest_chat()
        self.open_selected_edit_menu()
        self.click_change_chat_name()
        self.click_cancel_edit()
        self.open_selected_edit_menu()
        self.click_delete_chat()
        self.click_cancel_edit()
        
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

    # ================  main Chat ================ 
    def input_chat(self, text: str):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])      
        ChatInputController.send_text(textarea, text)
        self.click_send()  
        
    def action_user_chat(self, chat_key ,chat_type):    
        ai_input_lst = self.fm.read_json_file("ai_text_data.json")[chat_key]   
        for item in ai_input_lst:
            if item["type"] != chat_type:
                continue   

            self.input_chat(item["content"])
            self.wait_for_chat(stop = True, target = "ai")

    # ------------------- 채팅 메시지 기다리기 ---------------------------- 
    def wait_for_ai_complete(self, stop, target, timeout): 
        base_xpath = XPATH["MESSAGE_XPATH"][target]
        last_msg_xpath = f'({base_xpath}//div[@data-status])[last()]'
        
        start = time.time()
        while time.time() - start < timeout:
            #elem = self.get_element_by_xpath(last_msg_xpath)
            elems = self.get_elements_by_xpath(last_msg_xpath)

            if not elems:
                time.sleep(0.5)
                continue
            
            elem = elems[-1]
            if elem:
                status = elem.get_attribute("data-status")
                if status == "complete":
                    print(f"완료: : {elem.text}")
                    return AIresponse.COMPLETED
            time.sleep(0.5)
        return AIresponse.STOPPED if stop else AIresponse.TIMEOUT
    
    def wait_for_chat(self, stop, target, timeout = CHAT_TIME):
        result = self.wait_for_ai_complete(stop, target, timeout)
            
        match result:
            case AIresponse.STOPPED:
                btn = self.get_element_by_xpath(XPATH["BTN_STOP"])
                if btn and btn.is_enabled():
                    btn.click()
                    time.sleep(1)
                    return True    
            case AIresponse.COMPLETED:
                return True
            case AIresponse.TIMEOUT:
                return False                
                
    # ------------------- 채팅 보내고 비교 ---------------------------- 
    def compare_chats_after_user_send(self):
        prev_count = len(self.get_all_chats())
        print(prev_count)

        self.action_user_chat(ChatKey.INPUTS, ChatType.TEXT)

        after_count = len(self.get_all_chats())
        print(after_count)

        return prev_count != after_count
    
    # ------------------- action ---------------------------- 
    def click_send(self):
        self.click_btn_by_xpath(XPATH["BTN_SEND"], option = "presence")
        time.sleep(0.5)
    
    def click_btn_retry(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_RETRY"])
        if not btns:
            raise Exception("다시 생성하기 버튼이 없음.")
        
        btns[-1].click()
        return self.wait_for_chat(stop = True, target = "ai")
        
    # ================ Clipboard ================
    def get_last_user_message(self):
        xpath = f'({XPATH["MESSAGE_XPATH"]["user"]})[last()]'
        elem = self.get_element_by_xpath(xpath)
        return elem
 
    def force_hover(self, elem):
        self.driver.execute_script("""
            const el = arguments[0];
            el.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('mousemove', { bubbles: true }));
        """, elem)
    
    def get_user_last_tooltip(self, timeout=10):
        end = time.time() + timeout

        while time.time() < end:
            user_msg = self.get_last_user_message()
            if not user_msg:
                time.sleep(0.5)
                continue
            
            self.force_hover(user_msg)
            tooltips = self.get_elements_by_xpath(XPATH["TOOLTIP"])
            if tooltips:
                return tooltips[-1]
            time.sleep(0.5)
        return None
            
    # 추후 리팩토링 
    def copy_last_question(self):
        tooltip = self.get_user_last_tooltip()
        time.sleep(1)
        
        copy_btn = self.get_tooltip_button(tooltip, "복사")
        if copy_btn:
            self.driver.execute_script("arguments[0].click();", copy_btn)
        return ClipboardController.read()
    
    def paste_last_question(self):
        textarea = self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        ChatInputController.paste_text(textarea, self.copy_last_question())
        time.sleep(1)
    
    def get_tooltip_button(self, tooltip, aria_label, timeout=5):
        end = time.time() + timeout
        while time.time() < end:
            try:
                btn = tooltip.find_element(By.XPATH, f'.//button[@aria-label="{aria_label}"]')
                return btn
            except:
                time.sleep(0.2)
        return None
    
    # 추후 리팩토링 
    def smooth_scroll_into_view(self, elem):
        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        """, elem)
        time.sleep(0.8)
    
    def click_edit_last_question(self):
        user_msg = self.get_last_user_message()
        if not user_msg:
            return None

        self.smooth_scroll_into_view(user_msg)
        self.force_hover(user_msg)
        tooltip = self.get_user_last_tooltip()
        self.smooth_scroll_into_view(tooltip)

        edit_btn = tooltip.find_element(By.XPATH, XPATH["BTN_TOOLTIP_EDIT"])
        if edit_btn and edit_btn.is_enabled():
            self.driver.execute_script("arguments[0].click();", edit_btn)
            time.sleep(1)
        else:
            return False
        
    def send_after_edit_question(self):
        self.click_edit_last_question()
        
        ai_input_last = self.fm.read_json_file("ai_text_data.json")[ChatKey.RENAME][-1]
        content = ai_input_last["content"]
        
        textarea = self.get_element_by_xpath(XPATH["BTN_EDIT_AREA"])
        ClipboardController.copy(content)
        time.sleep(1)
        ChatInputController.reset_text(textarea)
        time.sleep(1)
        ClipboardController.paste(textarea)
        time.sleep(1) # 헝헝 너무 빨라서 time.sleep 했어요..
        
        btn_send = self.get_element_by_xpath(XPATH["BTN_EDIT_SEND"])
        if btn_send and btn_send.is_enabled():
            self.driver.execute_script("arguments[0].click();", btn_send)
            time.sleep(1)
            
        self.wait_for_chat(stop=True, target = "ai")

    def cancel_edit_question(self):
        self.click_edit_last_question()
        
        cancel_btn = self.get_element_by_xpath(XPATH["BTN_EDIT_CANCEL"])
        if cancel_btn and cancel_btn.is_enabled():
            self.driver.execute_script("arguments[0].click();", cancel_btn)
            time.sleep(1)
        
    
    def copy_last_response(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_COPY_RESPONE"])
        if not btns:
            raise Exception("복사 버튼이 없음.")

        btns[-1].click()
        time.sleep(0.5)
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
        # 메뉴 열기 버튼이 보이면 CLOSED 상태
        btn_open = self.get_element_by_xpath(XPATH["BTN_MENU_OPEN"])
        if btn_open and btn_open.is_displayed():
            self.menu_status = MenuStatus.CLOSED
            return

        # 메뉴 닫기 버튼이 보이면 OPENED 상태
        btn_close = self.get_element_by_xpath(XPATH["BTN_MENU_CLOSE"])
        if btn_close and btn_close.is_displayed():
            self.menu_status = MenuStatus.OPENED   

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
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_UPLOAD_FILE"], option = "visibility")
        ClipboardController.copy(file_path)
        ClipboardController.paste_file_path()

    def action_upload_file(self, file_path):
        self.paste_file_path_and_send(file_path)
        self.click_send()
        return self.wait_for_chat(stop = False, target = "ai")
            
    def upload_files(self):
        images = self.fm.get_asset_files(IMAGES_FORMAT)
        for img in images:
            self.action_upload_file(file_path = img)
            
        allowed_files = self.fm.get_asset_files(ENABLED_FORMAT)
        for file in allowed_files:
            self.action_upload_file(file_path = file)
        
        not_allowed_files = self.fm.get_asset_files(DISABLED_FORMAT)
        for file in not_allowed_files:
            self.action_upload_file(file_path = file)
    
    def upload_multi_files(self):
        files = self.fm.get_asset_files(MUITY_UPLOAD_FORMAT)
        files_sorted = sorted(files, key=lambda x: int(re.search(r'test_pdf_(\d+)\.pdf', x).group(1)))

        for file in files_sorted:
            self.paste_file_path_and_send(file)
        self.click_send()
        return self.wait_for_chat(stop = False, target = "ai")
 
    # ================ 이미지 생성 ================ 
    def action_gen_image(self):
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_GEN_IMAGE"], option = "visibility")


    # ================ 웹 검색 ================== 
    def action_search_web(self):
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_SEARCH_WEB"], option = "visibility")
        
        
    
    