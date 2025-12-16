from utils.headers import *
from utils.defines import XPATH, ID, SELECTORS

from enums.ui_status import MenuStatus
from pages.base_page import BasePage


class PastChatsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.past_chats = []
        
    def get_all_past_chats(self):
        return self.past_chats    
    
    def click_on_past_chat(self):
        items = self.get_elements_by_css_selector(SELECTORS["CHAT_LIST_ITEMS"])
        if not items:
            raise Exception("대화 내역이 없습니다.")

        # 인덱스 접근방식 대신, data-item들중 가장 큰 index를 선택하도록. (즉, 가장 밑 대화 클릭)
        latest = max(items, key=lambda x: int(x.get_attribute("data-item-index")))
        latest.click()
        time.sleep(1)  