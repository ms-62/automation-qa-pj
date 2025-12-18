from utils.headers import *
from utils.context import LoginContext
from utils.browser_utils import BrowserUtils
from utils.browser_setup import create_driver
from utils.context import LoginContext
from utils.defines import TARGET_URL

from managers.file_manager import FileManager
from pages.signup_page import SignupPage
 
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.member_page import MemberPage
from pages.agent_page import AgentPage
from pages.tools_page import ToolsPage
from pages.security_page import SecurityPage, SecurityMainPage
from test_logging.logging_config import setup_logging

# session = 하나의 드라이버 공유
@pytest.fixture(scope="session")
def driver():
    driver = create_driver()
    yield driver
    driver.quit()

# function = 테스트마다 새 드라이버 생성
@pytest.fixture(scope="function")
def signup_driver() :
    driver = create_driver()
    yield driver
    driver.quit()

    
@pytest.fixture
def fm():
    return FileManager()

@pytest.fixture
def main_page(driver):
    page = MainPage(driver)
    return page

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    return page

@pytest.fixture
def signup_page(signup_driver) :
    return SignupPage(signup_driver)

@pytest.fixture
def security_signup_page(signup_driver) :
    return SecurityPage(signup_driver)

@pytest.fixture
def security_main_page(driver) :
    page = SecurityMainPage(driver)
    return page

@pytest.fixture
def member_page(driver):
    page = MemberPage(driver)
    return page

@pytest.fixture
def agent_page(driver) :
    page = AgentPage(driver)
    return page

@pytest.fixture
def tools_page(driver) :
    page = ToolsPage(driver)
    return page



####### 메안화면 확인용 #######
@pytest.fixture
def user_data(fm):
    return fm.read_json_file("user_data.json")

@pytest.fixture

def logged_in_main(driver, fm, login_page, main_page, member_page, agent_page, user_data):
    ctx = LoginContext(
        driver=driver,
        fm=fm,
        login_page=login_page,
        main_page=main_page,
        member_page = member_page,
        agent_page = agent_page,
        user_data=user_data
    )
    
    browser_utils = BrowserUtils()
    return browser_utils.auto_login(ctx)

#memeber 테스트 데이터 받는 fixture: json 한 번만 읽는 용도
@pytest.fixture
def test_cases(fm):
    data = fm.read_json_file("member_test_data.json")
    return data or {}

#보안 테스트 데이터 받는 fixture
@pytest.fixture
def security_cases(fm):
    data = fm.read_json_file("security_data.json")
    return data or {}

# 수진 - 추가
@pytest.fixture
def logged_in_agent(driver, fm, login_page, main_page, member_page, agent_page, user_data):
    ctx = LoginContext(
        driver=driver,
        fm=fm,
        login_page=login_page,
        main_page=main_page,
        member_page=member_page,
        agent_page=agent_page,
        user_data=user_data
    )
    
    browser_utils = BrowserUtils()
    # loaded = browser_utils.load_cookies(
    #     driver=driver,
    #     fm=fm,
    #     url=TARGET_URL["MAIN_URL"],
    #     file_name="cookies.json"
    # )
    
    # if not browser_utils.is_logged_in(driver):
    browser_utils.auto_login(ctx)

    return agent_page

#logging 에러용으로 사용하려고
@pytest.fixture(scope="session", autouse=True)
def _setup_logging_once():
    setup_logging()