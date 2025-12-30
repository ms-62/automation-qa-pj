from utils.headers import *

from utils.defines import TIMEOUT_MAX
from managers.file_manager import FileManager
from controllers.mouse_controller import MouseController
import logging
    
logger = logging.getLogger()
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.fm = FileManager() 
        self.mouse = MouseController(self.driver)
        
    def go_to_page(self, url):
        self.driver.get(url)
        
    def find_element_presence_by_xpath(self, xpath, timeout=TIMEOUT_MAX):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            return None
    
    def get_element(self, by, value, option="presence", timeout=TIMEOUT_MAX):
        try:
            wait = WebDriverWait(self.driver, timeout)
            if option == "presence":
                return wait.until(EC.presence_of_element_located((by, value)))
            
            elif option == "visibility":
                return wait.until(EC.visibility_of_element_located((by, value)))
            
            elif option == "clickable":
                return wait.until(EC.element_to_be_clickable((by, value)))
        except (TimeoutException, NoSuchElementException):
            logger.error(f"element를 {by} = {value} 로 찾을 수 없음.")
            return None

    def get_element_by_id(self, id, option="presence", timeout = TIMEOUT_MAX):
        return self.get_element(By.ID, id, option, timeout)

    def get_element_by_name(self, name, option="presence", timeout = TIMEOUT_MAX):
        return self.get_element(By.NAME, name, option, timeout)

    def get_element_by_xpath(self, xp, option="presence", timeout = TIMEOUT_MAX):
        return self.get_element(By.XPATH, xp, option, timeout)
    
    def get_element_by_tag(self, tag, option="presence", timeout = TIMEOUT_MAX):
        return self.get_element(By.TAG_NAME, tag, option, timeout)

    def get_element_by_css_selector(self, cs, option="presence", timeout = TIMEOUT_MAX):
        return self.get_element(By.CSS_SELECTOR, cs, option, timeout)
    
    
    def get_elements(self, by, value, option="presence", timeout=TIMEOUT_MAX) :
        try :
            wait = WebDriverWait(self.driver, timeout)
            if option == "presence":
                elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            elif option == "visible":
                elements = wait.until(EC.visibility_of_all_elements_located((by, value)))
            else:
                elements = self.driver.find_elements(by, value)
            return elements
        except TimeoutException:
            logger.error(f"elements를 {by} = {value} 로 찾을 수 없음.")
            return []
        
    def get_elements_by_id(self, id, option="presence", timeout = TIMEOUT_MAX):
        return self.get_elements(By.ID, id, option, timeout)
    
    def get_elements_by_xpath(self, xp, option="presence", timeout = TIMEOUT_MAX):
        return self.get_elements(By.XPATH, xp, option, timeout)
    
    def get_elements_by_css_selector(self, cs, option = "presence", timeout = TIMEOUT_MAX):
        return self.get_elements(By.CSS_SELECTOR, cs, option, timeout)
    
    def debug_current_window_safe(self):
        """안전한 창 디버깅 (제목 없이 핸들만)"""
        current_handle = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        
        logger.info(f"현재 활성: {current_handle[:8]}...")
        logger.info(f"창 목록 ({len(all_handles)}개):")
        
        for i, handle in enumerate(all_handles):
            is_active = "✅" if handle == current_handle else "  "
            logger.info(f"  {i}: {is_active} {handle[:8]}...")
        
        return current_handle, all_handles
    def ensure_account_window(self, timeout=10):
        """계정 창 확인/전환 (이미 있으면 전환만)"""
        handles = self.driver.window_handles
        
        # 계정 페이지 URL 패턴
        account_patterns = ["accounts.elice.io", "member", "account"]
        
        for handle in handles:
            self.driver.switch_to.window(handle)
            current_url = self.driver.current_url
            
            # 계정 페이지면 전환 완료
            for pattern in account_patterns:
                if pattern in current_url:
                    logger.info(f"계정 창 발견: {current_url[:50]}")
                    self.debug_current_window_safe()
                    return True
        
        logger.error("계정 창 없음")
        return False

    #get_element 추가 보완 업데이트 - ci로 테스트 할 때 오류 발생 증가해서 보완
    def wait_for_element(self, by: By, value: str, timeout: float = 10, condition: str = "presence") -> object:
        wait = WebDriverWait(self.driver, timeout)
        locator = (by, value)
        
        try:
            # 1. 공통으로 '존재(Presence)'부터 먼저 확인 (가장 기본 단계)
            # clickable이나 visibility를 체크하기 전, DOM에 요소가 생길 때까지 잠시 대기
            element = wait.until(EC.presence_of_element_located(locator))

            # 2. 추가 조건 수행
            if condition == "visibility":
                return wait.until(EC.visibility_of_element_located(locator))
            elif condition in ["clickable", "enabled"]:
                # 존재함이 확인된 element 객체를 직접 전달하여 효율성 증대
                return wait.until(EC.element_to_be_clickable(element))
            
            # 기본값은 presence 결과 반환
            return element

        except TimeoutException:
            logger.error(f"요소 대기 실패: {by}={value} ({condition})")
            return None