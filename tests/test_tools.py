from utils.headers import *
from pages.tools_page import (ToolsPage)
from utils.browser_utils import (BrowserUtils)

def test_go_to_main(logged_in_main,tools_page):
    tools_page.go_to_main_page()