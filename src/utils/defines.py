import pyautogui
# define를 모으는 곳입니다.
# 각자 사용해야하는 selector나 xpath를 작성해주세요!

# 예시입니다!!
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
FULLSCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TIMEOUT_MAX = 10
STOPPED_MAX = 5
ACTIVE = "모델이 활성화되었습니다."
DEACTIVE = "모델이 비활성화되었습니다."
DEFAULT_MODEL = "Helpy Pro Agent"
DEFAULT_CHAT = "새 대화"

TARGET_URL = {
    "MAIN_URL": "https://qaproject.elice.io/ai-helpy-chat",
}


SELECTORS = {
    "BTNS_HOME_MENU" : 'a[href="/ai-helpy-chat"]',
    "MEMBER_MODAL" : "button.MuiAvatar-root.MuiAvatar-circular",
    "CHAT_LIST_ITEMS" : "a[data-item-index]",
    "BTN_SCROLL_TO_BOTTOM" : 'button[aria-label="맨 아래로 스크롤"]',
    "TEXTAREA" : "textarea[name='input']",
    "CHECK_CHAT_COMPLETE" : 'div[data-status="complete"]',
    "INPUT_MOBILE" : "input[name='to'][autocomplete='tel']",
    "BOX_LANG_ENG" : "ul[role='listbox'] li[data-value='en-US']",
    "BTN_MENU_BAR" : "button.EliceLayoutSidenavHamburger-root",
    
    # Agent 관련 파일 업로드 selector
    "IMAGE_FILE_INPUT": "input[type='file'][accept^='image']"
    

}

# By.ID
ID = {
    "CHECKBOX_HEADER" : "agreement-header",
    "SNACK_BAR" : "notistack-snackbar",
}

# By.NAME
NAME = {
    "INPUT_ID" : "loginId",    
    "INPUT_PW" : "password",  
    "INPUT_NAME" : "fullname",
    "BTN_MKT" : "marketing",
    "INPUT_NAME" : "fullname",
    "INPUT_EMAIL" : "to",
    "INPUT_PWD" :"password",
    "INPUT_NEW_PWD" : "newPassword",
}

# By.XPATH
XPATH = {
    "BTN_LOGIN": "//button[normalize-space()='Login']",
    "BTN_CREATE_ACCOUNT" : "//a[contains(@href, 'signup')]",
    "BTN_CREATE_EMAIL" : "//button",
    "SIGNUP_AGREE" : "//input[contains(@class, 'PrivateSwitchBase')]",
    "CHECK_SIGNUP" : "//a[contains(@href, 'recover')]",
    "BTN_SIGNUP" : "//button[@type = 'submit']",
    "BTN_MEMBER" : "//a[contains(@href,'account')]",
    "SIGNUP_FAIL" : "//p",
    "SCROLL_MAIN_CHAT" : "//div[contains(@class,'css-ovflmb')]",
    "BTN_UPLOAD" : "//svg[@data-testid='plusIcon']/parent::button",
    "BTN_SEND" : "//button[@aria-label='보내기']",
    "PASS_ELEMENT" : "//p[contains(text(), '통신사')]",
    "PASS_IFRAME" : "//iframe[contains(@src, 'certificates')]",
    "SIGNUP_VIEW_PW" : "//button[contains(@aria-controls, 'Password')]",

    "BTN_RETRY" : '//button[@aria-label="다시 생성"]',
    "BTN_COPY_RESPONE" : '//button[@aria-label="복사"]',
    
    #계정관리
    "BOX_LANG" : "//div[@aria-haspopup='listbox']",
    "SUBMIT_NAME" : "//button[@type='submit' and normalize-space(.)='완료']",
    "NAME_ROW": "//table[contains(@class,'css-69t54h')]//tr[td[normalize-space(.)='이름']]",
    "BTN_NAME_EDIT": "//tr[td[normalize-space(.)='이름']]//button[contains(@class,'MuiIconButton-root')]",
    "EMAIL_ROW" : "//table[contains(@class,'css-69t54h')]//tr[td[normalize-space(.)='이메일']]",
    "BTN_EMAIL_EDIT": "//tr[td[normalize-space(.)='이메일']]//button[contains(@class,'MuiIconButton-root')]",
    "BTN_CERTI_MAIL" : "//button[@type='submit' and normalize-space(.)='인증메일 발송']",
    "INVALID_MSG" : "//p[contains(@id,'helper-text')]",
    "MOBILE_ROW": "//table[contains(@class,'css-69t54h')]//tr[td[normalize-space(.)='휴대폰 번호']]",
    "BTN_MOBILE_EDIT" : "//tr[td[normalize-space(.)='휴대폰 번호']]//button[contains(@class,'MuiIconButton-root')]",
    "BTN_CERTI_MOBIL" : "//button[@type='submit' and contains(@class,'MuiLoadingButton-root')]",
    "TOAST_CONTAINER" : "//div[@role='alert'][@aria-describedby='notistack-snackbar']",
    "PWD_ROW" : "//table[contains(@class,'css-69t54h')]//tr[td[normalize-space(.)='비밀번호']]",
    "BTN_PWD_EDIT" : "//tr[td[normalize-space(.)='비밀번호']]//button[contains(@class,'MuiIconButton-root')]",
    "SUBMIT_PWD" : "//button[@type='submit' and normalize-space(.)='완료']",
    "BTN_OAUTH_KKO" : "//li[.//p[normalize-space(.)='카카오']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_GOOGLE" : "//li[.//p[normalize-space(.)='구글']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_GITHUB" : "//li[.//p[normalize-space(.)='깃허브']]//button[normalize-space(.)='연결하기']",
    "LANG_ROW" :  "//div[contains(@class,'MuiStack-root')][.//h2[normalize-space(.)='선호 언어']]",
    "SOCIAL_ROW" :  "//h2[contains(@class,'MuiTypography-body1')][normalize-space(.)='소셜 연결 계정']",
    
    "BTN_COPY_QUESTION" : "//div[@data-floating='true'])[last()]",
    "BTN_STOP" : '//button[@aria-label="취소"]',
    
    # 메인 화면 '메뉴' 확인용
    "BTN_MENU_OPEN": "//button[normalize-space(.)='메뉴 열기']",
    "BTN_MENU_CLOSE": "//button[normalize-space(.)='메뉴 접기']",
        
    # ai 모델
    "BTN_MODEL_DROPDOWN" : '//button[.//p[normalize-space()="{model_name}"]]',
    "MENU_PAPER": '//div[contains(@class,"MuiMenu-paper") and contains(@class,"MuiPopover-paper")]',  
    "MODEL_ITEMS": '//div[contains(@class,"MuiMenu-paper")]//li[@role="menuitem"]',
    "SELECTED_MODEL": '//button//p[contains(@class,"MuiTypography-body2")]',
    "MODEL_BY_NAME":'//div[contains(@class,"MuiMenu-paper")]''//li[@role="menuitem"]''[.//span[normalize-space()="{model_name}"]]',

    # # 모델 설정 창
    "BTN_MODEL_SETTING" : '//a[contains(@class,"MuiMenuItem-root") and .//span[normalize-space(text())="모델 설정"]]',
    "MODEL_LI": "//div[contains(@class, 'MuiStack-root') and contains(@class, 'css-8g8ihq')]//li[contains(@class,'MuiListItem-root')]",
    "MODEL_NAME_IN_LI" : ".//span[contains(@class,'MuiListItemText-primary')]",
    "MODEL_LI_BY_NAME" : '//li[.//span[contains(@class,"MuiListItemText-primary") and text()="{model_name}"]]',

    # li 내부 (상대 XPath)
    "MODEL_CHECKBOX": './/input[@type="checkbox"]',
    "MODEL_SWITCH": './/span[contains(@class,"MuiSwitch-switchBase")]',
    "MODEL_ALWAYS_ON": './/span[contains(@aria-label,"항상 활성화된 모델")]',

    # 팝업
    "MODEL_ENABLE_POPUP": '//div[@role="alert"]',
    
    # agent 메뉴
    "AGENT_MENU_BTN" : "//a[contains(@href, 'agents')]",
    "MY_AGENT_BTN" : "//a[contains(@href, 'mine')]",
    "AGENT_SEARCH" : "//input[@type = 'text']",
    "AGENT_SEARCH_RESULT" : "//p[contains(text(), 'project')]",
    "AGENT_SEARCH_NO_RESULT" : "//img[contains(@src, 'no_search')]",
    "AGENT_TALK" : "//a[contains(@class, 'MuiCard')]",
    "AGENT_TALK_CARD" : "//button[contains(@class, 'uy7nb7')]",
    "AGENT_TALK_CARD_TEXT" : "//button[contains(@class, 'uy7nb7')]//span",
    "AGENT_INPUT_TEXT" : "//span[@data-status = 'complete']",
    "NAME_SETT" : "//input[@name = 'name']",
    "INTRO_SETT" : "//input[@name = 'description']",
    "RULE_SETT" : "//textarea[@name = 'systemPrompt']",
    "CARD_SETT" : "//input[contains(@name, 'conversation')]",
    "GO_MAKE_AGENT" : "//a[contains(@href, 'builder')]",
    "BTN_AGENT_MAKE" : "//button[contains(@class, 'contained')]",
    "BTN_FOR_ME" : "//input[@value = 'private']",
    "BTN_FOR_AGENCY" : "//input[@value = 'organization']",
    "BTN_AGENT_PUBLISH" : "//button[contains(@form, 'publish')]",
    "CHECK_MAKE" : "//span[contains(@class, 'inherit')]",
    "ERROR_MSG" : "//p[contains(@class, 'error')]",
    "DELETE_CARD" : "//button[contains(@class, 'css-fyycg6')]",
    "SELECT_FUNCTION" : "//input[@type = 'checkbox']",
    "SCROLL_MAKE_AGENT" : "//div[contains(@class, 'css-1q1j9cm')]",
    "BTN_ADD_IMAGE" : "//button[contains(@class, 'css-807ylu')]",
    "BTN_MAKE_IMAGE" : "//li[@role = 'menuitem']",
    "UPLOADED_IMAGE_PREVIEW" : "//img[contains(@src, 'blob.core.windows.net')]",
    
    
    
    
    # 업로드 버튼
    "BTN_UPLOAD_FILE": "//li[.//span[text()='파일 업로드']]",
    "BTN_GEN_IMAGE": "//li[.//span[text()='이미지 생성']]",
    "BTN_SEARCH_WEB": "//li[.//span[text()='웹 검색']]",
    "FILE_INPUT" : "//input[@type='file']",
    
}

