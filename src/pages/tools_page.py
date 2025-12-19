from utils.headers import *

from pages.base_page import BasePage
from utils.defines import NAME,XPATH,SELECTORS,TARGET_URL
from selenium.webdriver.common.keys import Keys

class ToolsPage(BasePage):    
    ## 공용 메서드 ##
    def go_to_tools_page(self):
        self.get_element_by_xpath(XPATH["BTN_TOOLS"]).click()
        self.driver.implicitly_wait(0.3)
        
    # 학교 급 입력
    def select_school_class(self,school_class):
        btn = self.get_element_by_xpath(XPATH["SCHOOL_CLASS_DROPDOWN"])
        btn.click()
        self.driver.implicitly_wait(0.3)

        if school_class == "초등":
            btn = self.get_element_by_xpath(XPATH["ELEMENTARY_SCHOOL_CLASS"])
            btn.click()
            self.driver.implicitly_wait(0.3)
        elif school_class == "중등":
            btn = self.get_element_by_xpath(XPATH["MIDDLE_SCHOOL_CLASS"])
            btn.click()
            self.driver.implicitly_wait(0.3)
        elif school_class == "고등":
            btn = self.get_element_by_xpath(XPATH["HIGH_SCHOOL_CLASS"])
            btn.click()
            self.driver.implicitly_wait(0.3)
        else:
            raise ValueError("school_class는 '초등/중등/고등'만 가능합니다")
    
    # 과목 입력    
    def select_subject(self,school_class,subject_name):
        self.select_school_class(school_class)
        self.get_element_by_xpath(XPATH["SUBJECT_DROPDOWN"]).click()
        self.driver.implicitly_wait(0.3)
        
        subject_xpath = f"//li[normalize-space()='{subject_name}']"
        self.get_element_by_xpath(subject_xpath).click()
        self.driver.implicitly_wait(0.3)
    
    # 파일 업로드    
    def upload_file(self, file_path):
        file_input = self.get_element_by_xpath(XPATH["FILE_UPLOAD_INPUT"])
        file_input.send_keys(file_path)
        self.driver.implicitly_wait(0.3)
        
    # 파일 정상 업로드 시 UI 출력 
    def is_valid_upload_file(self):
        try:
            self.get_element_by_xpath(XPATH["VAILD_UPLOAD_FILE"])
            return True
        except:
            return False
        
    # 추가입력 칸 내용 입력
    def input_teacher_comment(self, add_data):
        element = self.get_element_by_name(NAME["TEACHER_COMMENT_AREA"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(add_data)
        self.driver.implicitly_wait(0.3)
                
    # 자동생성 버튼 클릭
    def click_auto_create_button(self):
        btn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, XPATH["BTN_AUTO_CREATE"])
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            btn
        )
        
        WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                (By.XPATH, XPATH["BTN_AUTO_CREATE"])
            )
        )
        btn.click()
        
    # 생성 중지 버튼 클릭
    def click_create_abort_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_CREATE_ABORT"])
        btn.click()
        self.driver.implicitly_wait(0.3)
    
    def is_create_abort_page(self):
        try:
            self.get_element_by_xpath(XPATH["CREATE_ABORT_MESSAGE"])
            return True
        except:
            return False
    
    # 다시생성 버튼 클릭 + 스크롤
    def click_recreate_button(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, XPATH["BTN_RECREATE"])
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            btn
        )
        
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, XPATH["BTN_RECREATE"])
            )
        )
        btn.click()
        
    # 결과 다시 생성하기 페이지 후 취소
    def click_create_reject_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_CREATE_REJECT"])
        btn.click()
        time.sleep(0.3)
    
    # 다시 생성 취소 후 다시 생성 버튼 활성화 확인
    def is_recreate_modal_open(self):
        return len(self.driver.find_elements(By.XPATH, XPATH["RECREATE_CONFIRM_MODAL"])) > 0
        
    # 결과 다시 생성하기 페이지 후 다시 생성
    def click_sure_recreate_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SURE_RECREATE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
    
    # 생성 결과 다운로드 버튼 클릭
    def click_download_result_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_RESULT"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    # 지원되지 않는 파일 에러메시지 출력 메서드
    def get_upload_error_text(self):
        el = self.get_element_by_xpath(XPATH["UPLOAD_ERROR_TEXT"])
        return el.text
    
    # 입력 양식 다운로드 버튼
    def click_download_template(self):
        btn = self.get_element_by_xpath(XPATH["DOWNLOAD_TEMPLATE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
            
    # 성취기준 검색하기 이동 버튼
    def click_achievement_button(self):
        btn = self.get_element_by_xpath(XPATH["BTN_ACHIEVEMENT"])
        btn.click()
        self.driver.implicitly_wait(0.3)
    
    # 성취기준 검색하기 URL 확인 메서드
    def switch_to_new_tab(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        self.driver.implicitly_wait(0.3)
    
    def is_achievement_page(self):
        url = self.driver.current_url
        return "stas.moe.go.kr" in url
    
    
    ## 세부 특기사항 탭 메서드 ##
    def click_special_note_page(self):
        btn = self.get_element_by_xpath(XPATH["BTN_SPECIAL_NOTE_PAGE"])
        btn.click()
        self.driver.implicitly_wait(0.3)   
    
    def is_special_note_page(self):
        try:
            self.get_element_by_xpath(XPATH["SPECIAL_NOTE_PAGE_TITLE"])
            return True
        except:
            return False
    
    ## 행동특성 및 종합의견 탭 메서드 ##
    def click_opinion_note_page(self):
        btn = self.get_element_by_xpath(XPATH["BTN_OPINION_NOTE_PAGE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def is_opinion_note_page(self):
        try:
            self.get_element_by_xpath(XPATH["OPINION_NOTE_PAGE_TITLE"])
            return True
        except:
            return False
    
    ## 수업지도안 탭 메서드 ##
    def click_teaching_note_page(self):
        btn = self.get_element_by_xpath(XPATH["BTN_TEACHING_NOTE_PAGE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def is_teaching_note_page(self):
        try:
            self.get_element_by_xpath(XPATH["TEACHING_NOTE_PAGE_TITLE"])
            return True
        except:
            return False
    
    # 정보 입력   
    def input_information(self,school_class,grade,subject_name,class_time):
        self.select_school_class(school_class)
        
        self.get_element_by_xpath(XPATH["GRADE_DROPDOWN"]).click()
        self.driver.implicitly_wait(0.3)
        grade_xpath = f"//li[normalize-space()='{grade}']"
        self.get_element_by_xpath(grade_xpath).click()
        self.driver.implicitly_wait(0.3)
        
        self.get_element_by_xpath(XPATH["SUBJECT_DROPDOWN"]).click()
        self.driver.implicitly_wait(0.3)
        subject_xpath = f"//li[normalize-space()='{subject_name}']"
        self.get_element_by_xpath(subject_xpath).click()
        self.driver.implicitly_wait(0.3)
        
        self.get_element_by_xpath(XPATH["CLASS_TIME"]).click()
        self.driver.implicitly_wait(0.3)
        class_time_xpath = f"//li[normalize-space()='{class_time}']"
        self.get_element_by_xpath(class_time_xpath).click()
        self.driver.implicitly_wait(0.3)
        
    # 성취기준 입력
    def input_achievement_standard(self,standard):
        element = self.get_element_by_name(NAME["ACHIEVEMENT_STANDARD_AREA"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(standard)
        self.driver.implicitly_wait(0.3)
    
    # 수업지도안 생성 결과 확인 메서드
    def is_teaching_result_valid(self):
        try:
            self.driver.find_elements((By.XPATH, XPATH["TEACHING_RESULT_VALID"]))
            return True
        except:
            return False
        
    ## PPT 탭 메서드 ##
    def click_create_ppt_page(self):
        btn = self.get_element_by_xpath(XPATH["BTN_CREATE_PPT_PAGE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def is_creat_ppt_page(self):
        try:
            self.get_element_by_xpath(XPATH["CREATE_PPT_PAGE_TITLE"])
            return True
        except:
            return False
    
    def ppt_input_information(self,topic,instruction,num_slide,num_section):
        element = self.get_element_by_name(NAME["TOPIC"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(topic)
        self.driver.implicitly_wait(0.3)
        
        element = self.get_element_by_name(NAME["INSTRUCTION"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(instruction)
        self.driver.implicitly_wait(0.3)
        
        element = self.get_element_by_name(NAME["PPT_NUM_SLIDE"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(num_slide)
        self.driver.implicitly_wait(0.3)
        
        element = self.get_element_by_name(NAME["PPT_NUM_SECTION"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(num_section)
        self.driver.implicitly_wait(0.3)
    
    def is_deepdive_on(self) -> bool:
        return len(self.driver.find_elements(By.XPATH, XPATH["ON_DEEP_DIVE"])) > 0
           
    def ppt_turn_on_deepdive(self):
        if not self.is_deepdive_on():
            self.get_element_by_name(NAME["BTN_DEEP_DIVE"]).click()
    
    def ppt_turn_off_deepdive(self):
        if self.is_deepdive_on():
            self.get_element_by_name(NAME["BTN_DEEP_DIVE"]).click()
    
    ## 퀴즈 생성 탭 메서드
    def click_create_quiz(self):
        btn = self.get_element_by_xpath(XPATH["BTN_CREATE_QUIZ"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def is_creat_quiz(self):
        try:
            self.get_element_by_xpath(XPATH["CREATE_QUIZ_TITLE"])
            return True
        except:
            return False
        
    def quiz_input_information(self,category,difficulty,topic):
        self.get_element_by_xpath(XPATH["CATEGORY_DROPDOWN"]).click()
        self.driver.implicitly_wait(0.3)
        category_xpath = f"//li[normalize-space()='{category}']"
        self.get_element_by_xpath(category_xpath).click()
        self.driver.implicitly_wait(0.3)
        
        self.get_element_by_xpath(XPATH["DIFFICULTY_DROPDOWN"]).click()
        self.driver.implicitly_wait(0.3)
        difficulty_xpath = f"//li[normalize-space()='{difficulty}']"
        self.get_element_by_xpath(difficulty_xpath).click()
        self.driver.implicitly_wait(0.3)
        
        element = self.get_element_by_name(NAME["QUIZ_TOPIC"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(topic)
        self.driver.implicitly_wait(0.3)
        
    def is_quiz_created(self):
        return len(self.driver.find_elements(By.XPATH, XPATH["QUIZ_RESULT"])) > 0
    
            
    ## 심층조사 탭 메서드 ##
    def click_create_deepdive(self):
        btn = self.get_element_by_xpath(XPATH["BTN_CREATE_DEEPDIVE"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
    def is_creat_deepdive(self):
        try:
            self.get_element_by_xpath(XPATH["CREATE_DEEPDIVE_TITLE"])
            return True
        except:
            return False
        
    def deepdive_input_information(self,topic,instruction):
        element = self.get_element_by_name(NAME["TOPIC"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(topic)
        self.driver.implicitly_wait(0.3)
        
        element = self.get_element_by_name(NAME["INSTRUCTION"])
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(instruction)
        self.driver.implicitly_wait(0.3)
        
    def click_deepdive_markdown_download_button(self):
        self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_RESULT"]).click()
        self.driver.implicitly_wait(0.3)
        
        btn = self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_MARKDOWN"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
        self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_RESULT"]).click()
        self.driver.implicitly_wait(0.3)
        
    def click_deepdive_HWP_download_button(self):
        self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_RESULT"]).click()
        self.driver.implicitly_wait(0.3)
        
        btn = self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_HWP"])
        btn.click()
        self.driver.implicitly_wait(0.3)
        
        self.get_element_by_xpath(XPATH["BTN_DOWNLOAD_DEEPDIVE_RESULT"]).click()
        self.driver.implicitly_wait(0.3)