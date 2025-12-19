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

        # 일단, 테스트를 위해서 검색 리스트에서 마지막 index로 지정
        # 만약 기존에 대화한 내역이 없다면?? fail로 처리할 것인가? 생각해보기 
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
        # WebDriverWait(self.driver, WAIT_TIME).until(
        #     EC.invisibility_of_element_located((By.CSS_SELECTOR, XPATH["BTN_SEARCH_CANCEL"]))
        # )
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
    

    # ---------------------------------- (12/19 회고용) 메인 챗 상단 햄버거메뉴 ----------------------------------- 
    # 1. 강제로 클릭 (기존대화내역은 마우스 action change 필요)
    # 2. rename_chat - 이전 메시지 이름과 '이름 편집' 기능 적용 후 이름 비교 -> 정확하게 바뀌었는지. 
    # 3. delete_chat - 이전 대화 리스트와 현재 리스트 개수 비교 -> 정확하게 삭제 되었는지. 
    # 4. cancel - 편집 중 취소, 삭제 중 취소 클릭 
    # -----------------------------------------------------------------------------------------------------
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
        prev_chats = self.get_all_chats()
        self.click_btn_by_xpath(XPATH["DELETE_NOWCHAT"], option="presence")
        self.click_delete_confirm()
        after_chats = self.get_all_chats()
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
        
    def click_btn_scroll_to_bottom(self, timeout = TIMEOUT_MAX):
        start = time.time()

        while time.time() - start < timeout:
            btn = self.get_element_by_css_selector(SELECTORS["BTN_SCROLL_TO_BOTTOM"])
            if btn and btn.is_enabled():
                try:
                    btn.click()
                    WebDriverWait(self.driver, WAIT_TIME).until(
                        lambda d: not btn.is_enabled()
                    )
                    return True
                except Exception:
                    pass

            #self.scroll_up_chat()
    
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
    # ResponseController 로는 안빼는 게 나을 것 같다.
    # ResponseController 에는 단순한 기능만. 
    # --------------------------------------------------------------------
    def wait_for_ai_complete(self, stop, target, timeout): 
        base_xpath = XPATH["MESSAGE_XPATH"][target]
        last_msg_xpath = f'({base_xpath}//div[@data-status])[last()]'
        
        start = time.time()
        elem = None
        while time.time() - start < timeout:            
            elems = self.get_elements_by_xpath(last_msg_xpath)

            if not elems:
                continue
            
            elem = elems[-1]
            if elem:
                status = elem.get_attribute("data-status")
                if status == "complete":
                    self.fm.save_json_file("ai_response_completed.json", {elem.text})
                    return AIresponse.COMPLETED
            time.sleep(0.5) ###
            
        if stop:
            # self.fm.save_json_file("ai_response_stopped.json", {elem.text}) -> [회고] element가 없으면?
            return AIresponse.STOPPED
        return AIresponse.TIMEOUT
    
    def wait_for_chat(self, stop, target, timeout = CHAT_TIME):
        result = self.wait_for_ai_complete(stop, target, timeout)
            
        match result:
            case AIresponse.STOPPED:
                btn = self.get_element_by_xpath(XPATH["BTN_STOP"])
                if btn and btn.is_enabled():
                    btn.click()
                    # 비활성화 되었는지 판별 후 return 또는 나중에 보내기 버튼이 활성화 되었는지 확인하는거로 바꿀것
                    time.sleep(0.5)
                    return True    
            case AIresponse.COMPLETED:
                return True
            case AIresponse.TIMEOUT:
                self.fm.save_screenshot_png(self.driver, "ai_response_timeout")
                return False                
                
    # ------------------- 채팅 보내고 비교 ---------------------------- 
    def compare_chats_after_user_send(self, chatkey = ChatKey.INPUTS, chatype = ChatType.TEXT):
        prev_count = len(self.get_all_chats())
        print(prev_count)

        self.action_user_chat(chatkey, chatype)

        after_count = len(self.get_all_chats())
        print(after_count)

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
    
    
    # =======================  Clipboard ==============================  
    # ------------------- 12/18 (회고용) 마우스를 이용해 강제로 편집창 보이게 해서 동작하게 함 ---------------------- 
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
        time.sleep(0.3)

    def get_user_last_tooltip(self, timeout=TIMEOUT_MAX):
        def _find_tooltip(driver):
            user_msg = self.get_last_user_message()
            if not user_msg:
                return False
            
            self.force_hover(user_msg)
            tooltips = self.get_elements_by_xpath(XPATH["TOOLTIP"])
            if tooltips:
                return tooltips[-1] 
            return False  
        return WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(_find_tooltip)    
            
    def copy_last_question(self):
        tooltip = WebDriverWait(self.driver, CHAT_TIME).until(
            lambda d: self.get_user_last_tooltip()  
        )
        copy_btn = self.get_tooltip_button(tooltip, "복사")
        if copy_btn:
            self.driver.execute_script("arguments[0].click();", copy_btn)
        return ClipboardController.read()
    
    def paste_last_question(self):
        textarea = WebDriverWait(self.driver, CHAT_TIME).until(
            lambda d: self.get_element_by_css_selector(SELECTORS["TEXTAREA"])
        )
        ChatInputController.paste_text(textarea, self.copy_last_question())

    def get_tooltip_button(self, tooltip, aria_label, timeout=CHAT_TIME):
        try:
            btn = WebDriverWait(tooltip, timeout, poll_frequency=0.1).until(
                lambda t: t.find_element(By.XPATH, f'.//button[@aria-label="{aria_label}"]')
            )
            return btn
        except TimeoutException:
            return None    

    def smooth_scroll_into_view(self, elem):   # 굳이 안해도 진행은 되지만, 화면에 보이게 하기 위해서 씀
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
        else:
            return False

        
    def send_after_edit_question(self):
        self.click_edit_last_question()

        ai_input_last = self.fm.read_json_file("ai_text_data.json")[ChatKey.RENAME][-1]
        content = ai_input_last["content"]

        textarea = WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: self.get_element_by_xpath(XPATH["BTN_EDIT_AREA"])
        )

        ChatInputController.reset_text(textarea)
        ClipboardController.copy(content)
        ClipboardController.paste(textarea)
        try:
            btn_send = WebDriverWait(self.driver, WAIT_TIME).until(EC.element_to_be_clickable((By.XPATH, XPATH["BTN_EDIT_SEND"])))
            self.driver.execute_script("arguments[0].click();", btn_send)
        except TimeoutException:
            print("Send button not clickable")
        self.wait_for_chat(stop=True, target="ai")
        
        
    def cancel_edit_question(self):
        self.click_edit_last_question()
        cancel_btn = self.get_element_by_xpath(XPATH["BTN_EDIT_CANCEL"])
        if cancel_btn and cancel_btn.is_enabled():
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

        # --------- (12/19) 사라진 기능 [회고용] ------------
        # btn_menu = self.get_element_by_xpath(XPATH["BTN_MENU_HAMBURGER"])
        # if btn_menu and btn_menu.is_displayed():
        #     self.menu_status = MenuStatus.CLOSED
        #     return
        # # 메뉴 닫기 버튼이 보이면 OPENED 상태
        # btn_close = self.get_element_by_xpath(XPATH["BTN_MENU_CLOSE"])
        # if btn_close and btn_close.is_displayed():
        #     self.menu_status = MenuStatus.OPENED   

    def toggle_menu(self, btn_element, staus):
        if not btn_element:
            return
        try:
            WebDriverWait(self.driver, WAIT_TIME).until(lambda d: btn_element.is_enabled())
            btn_element.click()
            if staus == MenuStatus.CLOSED:
                return MenuStatus.OPENED
            else:
                return MenuStatus.CLOSED
        except TimeoutException:
            print("버튼이 클릭 가능하지 않음")
            
        # --------- 사라진 기능 [회고용] ------------
        # def action_menu_arrow(self):
        #     if self.menu_status == MenuStatus.CLOSED: 
        #         btn_arrow = self.get_element_by_xpath(XPATH["BTN_MENU_OPEN"])
        #     else: 
        #         btn_arrow = self.get_element_by_xpath(XPATH["BTN_MENU_CLOSE"])
        #     self.toggle_menu(btn_arrow)

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





    
    