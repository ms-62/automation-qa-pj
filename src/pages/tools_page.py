from utils.headers import *

from pages.base_page import BasePage
from utils.defines import NAME,XPATH,SELECTORS,TARGET_URL

class ToolsPage(BasePage):
    def go_to_main_page(self):
        self.go_to_page(TARGET_URL["MAIN_URL"])
    
    def go_to_tools_page(self):
        self.go_to_page(TARGET_URL["TOOLS_URL"]) # 정의 필요
        
    # 세부 특기사항 관련 메서드
        # 세부 특기사항 클릭 메서드
        # 세부 특기사항 탭이 맞는지 메서드
        
    def select_school_class(self,school_class):
        btn = self.get_element_by_xpath(XPATH["SCHOOL_CLASS"]) # 정의 필요
        btn.click()
        time.sleep(0.3)

        if school_class == "초등":
            btn = self.get_element_by_xpath(XPATH["ELEMENTARY_SCHOOL_CLASS"]) # 정의 필요
            btn.click()
            time.sleep(0.3)
        elif school_class == "중등":
            btn = self.get_element_by_xpath(XPATH["MIDDLE_SCHOOL_CLASS"]) # 정의 필요
            btn.click()
            time.sleep(0.3)
        elif school_class == "고등":
            btn = self.get_element_by_xpath(XPATH["HIGH_SCHOOL_CLASS"]) # 정의 필요
            btn.click()
            time.sleep(0.3)
        else:
            raise ValueError("school_class는 '초등/중등/고등'만 가능합니다")
        
    def select_subject(self,school_class,subject_name):
        self.select_school_class(school_class)
        self.get_element_by_xpath(XPATH["SUBJECT_DROPDOWN"]).click() # 정의 필요
        time.sleep(0.3)
        
        subject_xpath = f"//li[normalize-space()='{subject_name}']"
        self.get_element_by_xpath(subject_xpath).click()
        time.sleep(0.3)
        
    def upload_data(self, file_path):
        file_input = self.get_element_by_xpath(XPATH["FILE_UPLOAD_INPUT"])  # 정의 필요
        file_input.send_keys(file_path)
    
    def input_add_data(self, add_data):
        element = self.get_element_by_name(NAME["ADD_DATA_AREA"])   # 정의 필요
        element.click()
        element.clear()
        element.send_keys(add_data)
        time.sleep(0.3)
        
    def click_auto_create_button(self):
        btn = self.get_element_by_xpath(XPATH["AUTO_CREATE"])   # 정의 필요
        btn.click()
        time.sleep(0.3)
        
    # 입력 양식 다운로드 버튼
    def click_form_download(self):
        btn = self.get_element_by_xpath(XPATH["FROM_DOWNLOAD"])
        btn.click()
        time.sleep(0.3)
        
    # 다운로드 확인 메서드
    
    # 성취기준 검색하기 이동 버튼
    
    # 성취기준 검색하기 URL 확인 메서드
    
    