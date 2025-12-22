from utils.headers import *
from utils.defines import XPATH, SELECTORS, ID, ACTIVE, DEACTIVE, DEFAULT_MODEL

from pages.base_page import BasePage
from enums.ui_status import ModelState

WAIT_TIME = 5

class ModelSettingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.active_models = None
        
    # ================ 드롭다운 메뉴 ================ 
    def open_model_menu(self):
        cur_model = self.get_current_model().strip()
        xpath = XPATH["BTN_MODEL_DROPDOWN"].format(model_name=cur_model)
        self.get_element_by_xpath(xpath, option="clickable").click()
        WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, XPATH["MODEL_ITEMS"]))
        )

    def is_dropdown_closed(self):
        el = self.get_element_by_xpath(XPATH["MENU_PAPER"], option="visibility")
        return el is None or not el.is_displayed()
    
    def get_all_model_names(self):
        items = self.get_elements_by_xpath(XPATH["MODEL_ITEMS"])
        return [item.text.strip() for item in items if item.text.strip()]

    def get_current_model(self): 
        el = self.get_element_by_xpath(XPATH["SELECTED_MODEL"])
        return el.text.strip()

    def select_last_model(self):    
        model_names = self.get_all_model_names()

        if len(model_names) > 1:
            model_name = model_names[-1]
        else:
            model_name = DEFAULT_MODEL

        xpath = XPATH["MODEL_BY_NAME"].format(model_name=model_name)
        self.get_element_by_xpath(xpath, option="clickable").click()

        WebDriverWait(self.driver, WAIT_TIME).until(
            lambda d: self.is_dropdown_closed()
        )
        selected = self.get_current_model()

        assert model_name in selected, "selected model 불일치"
    
    # ================ ai 모델 설정 화면 - 정보 가져오기 ================ 
    def go_to_model_setting(self):
        btn  = self.get_element_by_xpath(XPATH["BTN_MODEL_SETTING"], option="clickable")
        if btn and btn.is_enabled():
            btn.click()
        
    def get_all_models_in_setting(self):
        items = self.get_elements_by_xpath(XPATH["MODEL_LI"]) 
        models = []
        for li in items:
            name = li.find_element(By.XPATH, XPATH["MODEL_NAME_IN_LI"]).text.strip()
            models.append(name)
        return models
     
    def get_model_li(self, model_name: str):
        xpath = XPATH["MODEL_LI_BY_NAME"].format(model_name=model_name)
        return self.driver.find_element(By.XPATH, xpath)

    # ================ ai 모델 설정 화면 - 활성화 및 비활성화 ================ 
    def get_model_state(self, model_name: str):
        li = self.get_model_li(model_name)

        if li.find_elements(By.XPATH, XPATH["MODEL_ALWAYS_ON"]):
            return ModelState.ALWAYS_ON

        checkbox = li.find_element(By.XPATH, XPATH["MODEL_CHECKBOX"])

        return ModelState.ENABLED if checkbox.is_selected() else ModelState.DISABLED

    def enable_model(self, model_name: str):
        li = self.get_model_li(model_name)
        checkbox = li.find_element(By.XPATH, XPATH["MODEL_CHECKBOX"])

        if not checkbox.is_selected():
            checkbox.click()
            WebDriverWait(self.driver, WAIT_TIME).until(lambda d: checkbox.is_selected())

    def disable_model(self, model_name: str):
        li = self.get_model_li(model_name)
        checkbox = li.find_element(By.XPATH, XPATH["MODEL_CHECKBOX"])

        if checkbox.is_selected():
            checkbox.click()
            WebDriverWait(self.driver, WAIT_TIME).until(lambda d: not checkbox.is_selected())
            
    def verify_snackbar_message(self, expected_msg: str):
        try:
            snackbars = self.get_elements_by_id(ID["SNACK_BAR"])
            latest_snackbar = snackbars[-1]
            actual_msg = latest_snackbar.text.strip()
            expected_msg = expected_msg.strip()
            print(f"{actual_msg} == {expected_msg} ?")
            
            assert actual_msg == expected_msg, f"Snackbar 메시지 실패: {actual_msg} != {expected_msg}"
        except:
            raise AssertionError(f"{expected_msg} 메시지를 찾기 실패")
    
    def go_back(self):
        self.driver.back()       
    
    # ================== E2E - 버튼 클릭 후 정말로 정보가 변경되었는지 확인 ====================
    def toggle_all_models_and_verify(self):
        models = self.get_all_models_in_setting()

        self.active_models = []
        for model in models:
            initial_state = self.get_model_state(model)

            # 항상 활성화 모델은 건드리지 않음
            if initial_state == ModelState.ALWAYS_ON:
                self.active_models.append(model)
                continue

            if initial_state == ModelState.ENABLED:
                self.disable_model(model)
                self.verify_snackbar_message(DEACTIVE)
                
            elif initial_state == ModelState.DISABLED:
                self.active_models.append(model)
                self.enable_model(model)
                self.verify_snackbar_message(ACTIVE)
                
            # 상태가 바뀌었는지 검증
            actual_state = self.get_model_state(model)
            print(f"{model} 토글 : {initial_state} => {actual_state}")

    def compare_active_models(self):
        self.open_model_menu()
        models = self.get_all_model_names() 
        self.fm.save_screenshot_png(self.driver, "compare_activer_ai_models")
        assert models == self.active_models, f"active모델 일치하지 않음: {models} != {self.active_models}"
        
