from utils.headers import *

from pages.base_page import BasePage
from utils.defines import NAME,XPATH,SELECTORS,TARGET_URL

class ToolsPage(BasePage):
    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])