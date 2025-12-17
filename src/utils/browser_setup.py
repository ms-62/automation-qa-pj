from utils.headers import *
from utils.defines import FULLSCREEN_SIZE

def create_driver(browser="chrome"):
    
    browser = browser.lower()
    if browser == "chrome":
       
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "detach", False
        )  
        
         # 성진 추가: 다운로드 경로 고정 
        download_path = os.path.abspath("src/resources/downloads")

        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # 드라이버 옵션 설정
        chrome_options.add_argument("--start-maximized")  
        chrome_options.add_argument("--disable-autofill")
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_argument("--disable-password-manager-reauthentication")
        chrome_options.add_argument("--disable-extensions")

        # 드라이버 자동 설치 및 서비스 설정
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
    elif browser == "safari":
        # safari는 옵션이 필요없으나 환경설정 -> 개발자 메뉴 -> 원격 자동화 옵션 허용이 필요하다고합니다!
        try:
            driver = webdriver.Safari()
            driver.set_window_size(*FULLSCREEN_SIZE) # maximized 옵션 없음
        except Exception as e:
            print("Safari webdriver 실패 원격자동화 옵션을 확인해주세요.") 
            raise e
    else:
        raise ValueError(f"지원하지 않는 브라우저입니다 = {browser}")
    
    return driver
