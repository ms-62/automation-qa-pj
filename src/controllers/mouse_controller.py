from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

class MouseController:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)

    def move(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def move_and_click(self, move_el, click_el):
        self.move(move_el)
        self.click(click_el)