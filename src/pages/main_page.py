from utils.headers import *
import re
from pages.base_page import BasePage
from utils.defines import SELECTORS, XPATH, TARGET_URL, TIMEOUT_MAX

from enums.ui_status import MenuStatus, AIresponse
from utils.defines import ChatKey, ChatType, ChatMenu
from states.response_state import ResponseState

from controllers.chat_input_controller import ChatInputController
from controllers.clipboard_controller import ClipboardController
from controllers.response_controller import ResponseController
from controllers.scroll_controller import ScrollController

from selenium.webdriver.common.action_chains import ActionChains

CHAT_TIME = 10
WAIT_TIME = 5
MINI_SCROLL_STEP = 200

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  

    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])

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
        chat_items = WebDriverWait(self.driver, WAIT_TIME, poll_frequency=0.1).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, SELECTORS["SEARCH_CHAT_ITEMS"]))
        )
        return chat_items
        
    def get_first_chat_name(self, chat_item):
        if not chat_item:
            return None
        return chat_item.get_attribute("innerText").strip() or None
    
    def search_past_chats_by_click(self):
        chat_items = self.get_search_chat_items()
        if not chat_items:
            return False

        first_item = chat_items[-1] 
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable(first_item)
        )
        self.driver.execute_script("arguments[0].click();", first_item)

        # 서치 완료된건지 알기위해 btn_cancel이 사라졌는지 
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, XPATH["BTN_SEARCH_CANCEL"]))
        )
        return True
    
    def get_after_search_chat_items(self):
        input_search = self.get_element_by_xpath(XPATH["INPUT_SEARCH_CHAT"], option="clickable")

        chat_item = self.get_search_chat_items()[-1] if self.get_search_chat_items() else None
        if not chat_item:
            return False

        chat_name = self.get_first_chat_name(chat_item=chat_item)
        if not chat_name:
            return False

        ChatInputController.send_text(input_search, chat_name)

        # 검색해서, 채팅내역이 나온다면 
        WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: len(self.get_search_chat_items()) > 0
        )
        after_chat_items = self.get_search_chat_items()
        return after_chat_items
    
    def search_past_chats_by_input(self):
        after_chat_items = self.get_after_search_chat_items()
        if not after_chat_items:
            return False

        chat_item = after_chat_items[0] 
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable(chat_item)
        )
        self.driver.execute_script("arguments[0].click();", chat_item)
        
        # 서치 완료된건지 알기위해 btn_cancel이 사라졌는지 
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, XPATH["BTN_SEARCH_CANCEL"]))
        )
        return True
    
    def scroll_up_search(self):
        area = self.find_element_presence_by_xpath(XPATH["SCROLL_SEARCH_AREA"])
        if not area:
            return False
        ScrollController.scroll_up(self.driver, area, step = MINI_SCROLL_STEP)
        return True
    
    def scroll_down_search(self):
        area = self.find_element_presence_by_xpath(XPATH["SCROLL_SEARCH_AREA"])
        if not area:
            return False
        ScrollController.scroll_down(self.driver, area, step = MINI_SCROLL_STEP)
        return True
    

    # ---------------------------------- 메인 챗 상단 햄버거메뉴 ----------------------------------- 
    def click_main_chat_hamburger(self):
        self.select_latest_chat()
        btn = WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: d.execute_script("""
                const el = document.querySelector("div.css-16qm689 button svg[data-testid='ellipsis-verticalIcon']");
                return el ? el.parentElement : null;
            """)
        )
        self.driver.execute_script("arguments[0].click();", btn)
    
    def rename_main_chat(self):
        self.click_main_chat_hamburger()
        self.click_btn_by_xpath(XPATH["CHANGE_NOWCHAT_NAME"], option="presence")
        self.action_rename_chat()

        
    def delete_main_chat(self):
        self.click_main_chat_hamburger()
        prev_chats = len(self.get_all_chats()) 
        self.click_btn_by_xpath(XPATH["DELETE_NOWCHAT"], option="presence")
        self.click_delete_confirm()
        after_chats = len(self.get_all_chats())
        return False if prev_chats == after_chats else True 
    
    
    # ================ past_chat_page (기존 대화 내용 기록) ================ #
    def get_selected_chat(self):
        selected_item = self.get_element_by_css_selector(SELECTORS["SELECTED_CHAT"])
        return selected_item

    def get_selected_chat_name(self):
        selected_text = self.get_element_by_css_selector(SELECTORS["SELECTED_CHAT_TEXT"], option="visibility").text.strip()
        return selected_text

    def get_all_chats(self):
        return self.get_elements_by_css_selector(SELECTORS["CHAT_LIST_ITEMS"])

    def compare_prev_and_after_chats(self, prev_chats_texts):
        WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: [chat.text for chat in self.get_all_chats()] != prev_chats_texts
        )
        after_chats_texts = [chat.text for chat in self.get_all_chats()]
        return prev_chats_texts != after_chats_texts

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
        if not area:
            return False
        ScrollController.scroll_up(self.driver, area, step = MINI_SCROLL_STEP)
        return True

    def scroll_down_past_chats(self):
        area = self.get_element_by_xpath(XPATH["SCROLL_PAST_CHATS"])
        if not area:
            return False
        ScrollController.scroll_down(self.driver, area, step = MINI_SCROLL_STEP)
        return True


    # ---------- E2E 용도 ----------
    def rename_past_chats(self):
        self.open_selected_edit_menu()
        self.click_change_chat_name()
        self.action_rename_chat()
    
    def action_rename_chat(self):
        name_area = self.get_element_by_css_selector(SELECTORS["INPUT_CHAT_NAME"])
        name_area.click()
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
        prev_chats = len(self.get_all_chats())
        self.open_selected_edit_menu()
        self.click_delete_chat()
        self.click_delete_confirm()
        after_chats = len(self.get_all_chats())
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
    def get_main_screen_area(self):
        area = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS["SCROLL_MAIN_CHAT_"]))
        )
        return area
    
    def scroll_up_chat(self):
        area = self.get_main_screen_area()
        if not area:
            return False
        ScrollController.scroll_up(self.driver, area)
        return True 
    
    def scroll_down_chat(self):
        area = self.get_main_screen_area()
        if not area:
            return False
        ScrollController.scroll_down(self.driver, area)
        return True 
    
    def click_btn_scroll_to_bottom(self, timeout=TIMEOUT_MAX):
        start = time.time()

        while time.time() - start < timeout:
            try:
                btn = self.get_element_by_css_selector(
                    SELECTORS["BTN_SCROLL_TO_BOTTOM"],
                    option="presence"
                )
            except Exception:
                btn = None

            if btn and btn.is_displayed() and btn.is_enabled():
                btn.click()

                WebDriverWait(self.driver, WAIT_TIME).until(
                    lambda d: not btn.is_displayed() or not btn.is_enabled()
                )
                return True

            self.driver.execute_script("""
                const el = document.scrollingElement || document.documentElement;
                el.scrollTop = Math.max(0, el.scrollTop - 300);
            """)

        return False
    
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

    # ----------------------- 채팅 메시지 기다리기 ---------------------------- 
    def wait_chat_idle(self, timeout=WAIT_TIME): # 중단 버튼이 안보일때까지 
        WebDriverWait(self.driver, timeout, poll_frequency=0.3).until(
        EC.invisibility_of_element_located((By.XPATH, XPATH["BTN_STOP"]))
    )
    
    def wait_for_ai_complete(self, stop = False, target = "ai", timeout=CHAT_TIME):
        base_xpath = XPATH["MESSAGE_XPATH"][target]
        last_msg_xpath = f'({base_xpath}//div[@data-status])[last()]'
        
        try:
            elem = WebDriverWait(self.driver, timeout, poll_frequency=0.3).until(
                lambda d: (
                    (els := self.get_elements_by_xpath(last_msg_xpath))
                    and els[-1].get_attribute("data-status") == "complete"
                    and els[-1]
                )
            )
            self.fm.save_json_file("ai_response_completed.json", {elem.text})
            return AIresponse.COMPLETED
        except TimeoutException:
            return AIresponse.STOPPED if stop else AIresponse.TIMEOUT
    
    def wait_for_chat(self, stop, target, timeout = CHAT_TIME):
        result = self.wait_for_ai_complete(stop, target, timeout)
            
        match result:
            case AIresponse.STOPPED:
                btn = self.get_element_by_xpath(XPATH["BTN_STOP"])
                if btn and btn.is_enabled():
                    btn.click()
                    return True
            case AIresponse.COMPLETED:
                    return True
            case AIresponse.TIMEOUT:
                self.fm.save_screenshot_png(self.driver, "ai_response_timeout")
                return False                
                
    # ------------------- 채팅 보내고 비교 ---------------------------- 
    def compare_chats_after_user_send(self, chatkey = ChatKey.INPUTS, chatype = ChatType.TEXT):
        prev_count = len(self.get_all_chats())

        self.action_user_chat(chatkey, chatype)

        after_count = len(self.get_all_chats())

        return prev_count != after_count
    
    # ------------------- action ---------------------------- 
    def click_send(self):
        self.click_btn_by_xpath(XPATH["BTN_SEND"], option = "presence")
    
    def click_btn_retry(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_RETRY"])
        if not btns:
            raise Exception("다시 생성하기 버튼이 없음.")
        
        btns[-1].click()
        return self.wait_for_chat(stop = True, target = "ai")
    

    # ------------------- 마우스를 이용해 강제로 편집창 보이게 해서 동작하게 함 --------------------
    def get_last_user_message(self):
        xpath = f'({XPATH["MESSAGE_XPATH"]["user"]})[last()]'
        try:
            return self.get_element_by_xpath(xpath)
        except TimeoutException:
            return None


    def force_hover(self, elem):
        self.driver.execute_script("""
            const el = arguments[0];
            el.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
            el.dispatchEvent(new MouseEvent('mousemove', { bubbles: true }));
        """, elem)


    def smooth_scroll_into_view(self, elem):
        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                behavior: 'instant',
                block: 'center'
            });
        """, elem)


    # ======================
    # Tooltip 관련
    # ======================

    def get_user_last_tooltip(self, timeout=WAIT_TIME):
        def _find(driver):
            try:
                user_msg = self.get_last_user_message()
                if not user_msg:
                    return False

                self.smooth_scroll_into_view(user_msg)
                self.force_hover(user_msg)

                tooltips = self.get_elements_by_xpath(XPATH["TOOLTIP"])
                if tooltips:
                    return tooltips[-1]

                return False
            except StaleElementReferenceException:
                return False

        return WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(_find)


    def get_tooltip_button(self, tooltip, aria_label, timeout=WAIT_TIME):
        def _find_btn(driver):
            try:
                return tooltip.find_element(
                    By.XPATH, f'.//button[@aria-label="{aria_label}"]'
                )
            except StaleElementReferenceException:
                return False

        try:
            return WebDriverWait(self.driver, timeout, poll_frequency=0.1).until(_find_btn)
        except TimeoutException:
            return None


    # ======================
    # Tooltip 액션 통합 (핵심)
    # ======================

    def click_user_tooltip_button(self, aria_label, timeout=WAIT_TIME):
        def _click(driver):
            try:
                tooltip = self.get_user_last_tooltip()
                btn = self.get_tooltip_button(tooltip, aria_label)
                if not btn:
                    return False

                driver.execute_script("arguments[0].click();", btn)
                return True
            except StaleElementReferenceException:
                return False

        WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(_click)


    # ======================
    # 질문 복사 / 붙여넣기
    # ======================

    def copy_last_question(self):
        self.click_user_tooltip_button("복사")
        return ClipboardController.read()


    def paste_last_question(self):
        textarea = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["TEXTAREA"]))
        )
        ChatInputController.paste_text(textarea, self.copy_last_question())


    # ======================
    # 편집 관련
    # ======================

    def click_edit_last_question(self):
        self.click_user_tooltip_button("수정")


    def send_after_edit_question(self):
        self.click_edit_last_question()

        textarea = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.visibility_of_element_located((By.XPATH, XPATH["BTN_EDIT_AREA"]))
        )

        ai_input_last = self.fm.read_json_file("ai_text_data.json")[ChatKey.RENAME][-1]
        content = ai_input_last["content"]

        ChatInputController.reset_text(textarea)
        ClipboardController.copy(content)
        ClipboardController.paste(textarea)

        send_btn = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, XPATH["BTN_EDIT_SEND"]))
        )
        self.driver.execute_script("arguments[0].click();", send_btn)

        self.wait_for_chat(stop=True, target="ai")


    def cancel_edit_question(self):
        self.click_edit_last_question()

        cancel_btn = WebDriverWait(self.driver, WAIT_TIME).until(
            EC.element_to_be_clickable((By.XPATH, XPATH["BTN_EDIT_CANCEL"]))
        )
        self.driver.execute_script("arguments[0].click();", cancel_btn)
            
    # ------------------- action ---------------------------- 
     
    def copy_last_response(self):
        btns = self.get_elements_by_xpath(XPATH["BTN_COPY_RESPONE"])
        if not btns:
            raise Exception("복사 버튼이 없음.")

        last_btn = btns[-1]

        try:
            WebDriverWait(self.driver, WAIT_TIME).until(lambda d: last_btn.is_enabled())
            last_btn.click()
        except TimeoutException:
            raise Exception("복사 버튼이 클릭 가능하지 않음.")
        return ClipboardController.read()
 
    
    def paste_last_response(self):
        textarea = WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: self.get_element_by_css_selector(SELECTORS["TEXTAREA"]) 
            if self.get_element_by_css_selector(SELECTORS["TEXTAREA"]).is_enabled() 
            else None
        )
        ChatInputController.paste_text(textarea, self.copy_last_response())

    
    def reset_chat(self):
        textarea = WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: self.get_element_by_css_selector(SELECTORS["TEXTAREA"]) 
            if self.get_element_by_css_selector(SELECTORS["TEXTAREA"]).is_enabled() 
            else None
        )
        ChatInputController.reset_text(textarea)

    # ------------  버튼 요소 변화, 동작 변화로 수정 -----------
    # 사이드바가 열리는지 안열리는지로 메뉴가 open되었나 안되었나 판단. 
    # ================  메뉴 ================ 
    def is_side_menu_open_by_layout(self, link_elem):
        height = self.driver.execute_script(
            "return arguments[0].getBoundingClientRect().height;",
            link_elem
        )
        return height > 0

    def get_side_menu_status(self):
        link = self.find_element_presence_by_xpath(XPATH["BTN_PLAN"], timeout = WAIT_TIME)

        if not link:
            return MenuStatus.CLOSED
        if not self.is_side_menu_open_by_layout(link):
            return MenuStatus.CLOSED
        return MenuStatus.OPENED

    def toggle_menu(self, btn_element, staus):
        if not btn_element:
            return 
        
        WebDriverWait(self.driver, WAIT_TIME).until(lambda d: btn_element.is_enabled())
        btn_element.click()
        if staus == MenuStatus.CLOSED:
            return MenuStatus.OPENED
        else:
            return MenuStatus.CLOSED
            
    def action_menu_bar(self):
        status = self.get_side_menu_status()
        btn = self.get_element_by_xpath(XPATH["BTN_MENU_HAMBURGER"])
        return self.toggle_menu(btn, status)
        
    
    #================ 파일 업로드 ================ 
    def open_upload_file_dialog(self):
        plus = self.get_element_by_css_selector(SELECTORS["BTN_UPLOAD_PLUS_CSS"])
        if plus and plus.is_enabled():
            plus.click()

    def paste_file_path_finder(self, file_path):   
        self.open_upload_file_dialog()
        self.click_btn_by_xpath(XPATH["BTN_UPLOAD_FILE"], option = "visibility")
        ClipboardController.copy(file_path)
        ClipboardController.paste_file_path(file_path)

    def upload_files(self, format):
        files = self.fm.get_asset_files(format)
        if not files:
            return False 
        
        for file in files:
            self.paste_file_path_finder(file)
            self.click_send()
            ResponseController.wait_for_response_with_timeout(btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]), stop_time=CHAT_TIME)
            
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS["BTN_UPLOAD_PLUS_CSS"]))
            )
        return True     
            
    def upload_multi_files(self):
        files = self.fm.get_asset_files(".pdf")
        if not files:
            return False 
        
        matched_files = []
        for f in files:
            filename = os.path.basename(f)
            match = re.search(r'test_pdf_(\d+)\.pdf', filename)
            if match:
                matched_files.append((f, int(match.group(1))))
        
        files_sorted = [f for f, _ in sorted(matched_files, key=lambda x: x[1])]
        results = []

        for file in files_sorted:
            res = self.paste_file_path_finder(file_path=file)
            results.append(res)

        self.click_send()
        ResponseController.wait_for_response_with_timeout(btn_stop=lambda: self.get_element_by_xpath(XPATH["BTN_STOP"]), stop_time=CHAT_TIME)
        return True 





    
    