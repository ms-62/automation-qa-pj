from utils.headers import *

from pages.base_page import BasePage
from utils.defines import NAME,XPATH,SELECTORS,TARGET_URL

class ToolsPage(BasePage):    
    def go_to_tools_page(self):
        self.get_element_by_xpath(XPATH["BTN_TOOLS"]).click()
        time.sleep(0.3)
        
    ## 세부 특기사항 관련 메서드
    # 세부 특기사항 클릭 메서드
    def click_special_note_page(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SPECIAL_NOTE_PAGE"])
        btn.click()
        time.sleep(0.3)   
    
    # 세부 특기사항 탭이 맞는지 메서드
    def is_special_note_page(self):
        try:
            self.get_element_by_xpath(XPATH["SPECIAL_NOTE_PAGE_TITLE"])
            return True
        except:
            return False
    
    # 학교 급 입력
    def select_school_class(self,school_class):
        btn = self.get_element_by_xpath(XPATH["SCHOOL_CLASS_DROPDOWN"])
        btn.click()
        time.sleep(0.3)

        if school_class == "초등":
            btn = self.get_element_by_xpath(XPATH["ELEMENTARY_SCHOOL_CLASS"])
            btn.click()
            time.sleep(0.3)
        elif school_class == "중등":
            btn = self.get_element_by_xpath(XPATH["MIDDLE_SCHOOL_CLASS"])
            btn.click()
            time.sleep(0.3)
        elif school_class == "고등":
            btn = self.get_element_by_xpath(XPATH["HIGH_SCHOOL_CLASS"])
            btn.click()
            time.sleep(0.3)
        else:
            raise ValueError("school_class는 '초등/중등/고등'만 가능합니다")
    
    # 과목 입력    
    def select_subject(self,school_class,subject_name):
        self.select_school_class(school_class)
        self.get_element_by_xpath(XPATH["SUBJECT_DROPDOWN"]).click()
        time.sleep(0.3)
        
        subject_xpath = f"//li[normalize-space()='{subject_name}']"
        self.get_element_by_xpath(subject_xpath).click()
        time.sleep(0.3)
    
    # 파일 업로드    
    def upload_data(self, file_path):
        file_input = self.get_element_by_xpath(XPATH["FILE_UPLOAD_INPUT"])  # 정의 필요
        file_input.send_keys(file_path)
        time.sleep(0.3)
    
    # 추가입력 칸 내용 입력
    def input_teacher_comment(self, add_data):
        element = self.get_element_by_name(NAME["TEACHER_COMMENT_AREA"])
        element.click()
        element.clear()
        element.send_keys(add_data)
        time.sleep(0.3)
                
    # 자동생성 버튼 클릭
    def click_auto_create_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_AUTO_CREATE"])
        btn.click()
        time.sleep(0.3)
        
    # 생성 중지 버튼 클릭
    def click_create_abort_button(self):
        self.get_element_by_xpath(XPATH["BTN_CREATE_ABORT"])
        time.sleep(0.3)
    
    def is_create_abort_page(self):
        try:
            self.get_element_by_xpath(XPATH["CREATE_ABORT_MESSAGE"])
            return True
        except:
            return False
    
    # 다시생성 버튼 클릭
    def click_recreate_button(self):
        self.get_element_by_xpath(XPATH["BTN_RECREATE"])
        time.sleep(0.3)
        
    # 결과 다시 생성하기 페이지 후 취소
    def click_create_reject_button(self):
        self.get_element_by_xpath(XPATH["BTN_CREATE_REJECT"])
        time.sleep(0.3)
        
    # 결과 다시 생성하기 페이지 후 다시 생성
    def click_sure_recreate_button(self):
        self.get_element_by_xpath(XPATH["BTN_SURE_RECREATE"])
        time.sleep(0.3)
    
    # 생성 결과 다운로드 버튼 클릭
    def click_download_result_button(self):
        self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_RESULT"])  # 정의 필요
        time.sleep(0.3)
        
    # 지원되지 않는 파일 메서드 -> 근데 지금 웹 상에서 반응이 없음
    def get_upload_error_text(self):
        el = self.get_element_by_xpath(XPATH["UPLOAD_ERROR"])  # 정의 필요 에러 토스트/헬퍼텍스트 xpath
        return el.text
    
    def is_upload_error_visible(self):
        try:
            self.get_element_by_xpath(XPATH["UPLOAD_ERROR"]) 
            return True
        except:
            return False
       
    # 입력 양식 다운로드 버튼
    def click_download_template(self):
        btn = self.get_element_by_xpath(XPATH["DOWNLOAD_TEMPLATE"])
        btn.click()
        time.sleep(0.3)
            
    # 성취기준 검색하기 이동 버튼
    def click_achievement_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_ACHIEVEMENT"])
        btn.click()
        time.sleep(0.3)
    
    # 성취기준 검색하기 URL 확인 메서드
    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        time.sleep(0.3)
    
    def is_achievement_page(self):
        url = self.driver.current_url
        return "stas.moe.go.kr" in url