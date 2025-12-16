import pyautogui
# define를 모으는 곳입니다.
# 각자 사용해야하는 selector나 xpath를 작성해주세요!

# 예시입니다!!
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
FULLSCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TIMEOUT_MAX = 10
STOPPED_MAX = 7
ACTIVE = "모델이 활성화되었습니다."
DEACTIVE = "모델이 비활성화되었습니다."
DEFAULT_MODEL = "Helpy Pro Agent"
DEFAULT_CHAT = "새 대화"

TARGET_URL = {
    "MAIN_URL": "https://qaproject.elice.io/ai-helpy-chat",
    "LOGIN_URL": "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
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

    "BOX_LANG_KOR" : "ul[role='listbox'] li[data-value='ko-KR']",
    
    # Agent 관련 파일 업로드 selector
    "IMAGE_FILE_INPUT": "input[type='file'][accept^='image']",
    "FILE_INPUT" : "input[type='file'][accept*='.pdf']",
    "FILE_INPUT_IN_CHAT" : "input[type='file']",
    

    "BTNS_DISABLED" : "button.MuiIconButton-root:not([disabled])",
    "BTN_PLUS" : "svg[data-icon='plus']",
    "BTN_UPLOAD_PLUS_CSS" : "button.MuiIconButton-root:not([disabled]) svg[data-icon='plus']",


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
    "BTN_UPLOAD_PLUS" : "//button[contains(@class,'MuiIconButton-root') and .//svg[@data-icon='plus']]",
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
    "TOAST_CONTAINER" : "//div[@id='notistack-snackbar']",
    "PWD_ROW" : "//table[contains(@class,'css-69t54h')]//tr[td[normalize-space(.)='비밀번호']]",
    "BTN_PWD_EDIT" : "//tr[td[normalize-space(.)='비밀번호']]//button[contains(@class,'MuiIconButton-root')]",
    "SUBMIT_PWD" : "//button[@type='submit' and normalize-space(.)='완료']",
    "BTN_OAUTH_GOOGLE" : "//li[.//p[normalize-space(.)='구글']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_NAVER" : "//li[.//p[normalize-space(.)='네이버']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_KKO" : "//li[.//p[normalize-space(.)='카카오']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_GITHUB" : "//li[.//p[normalize-space(.)='깃허브']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_APPLE" : "//li[.//p[normalize-space(.)='애플']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_FACEBOOK" : "//li[.//p[normalize-space(.)='페이스북']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_WHALESPACE" : "//li[.//p[normalize-space(.)='웨일스페이스']]//button[normalize-space(.)='연결하기']",
    "BTN_OAUTH_MICROSOFT" : "//li[.//p[normalize-space(.)='마이크로소프트']]//button[normalize-space(.)='연결하기']",
    "LANG_ROW" :  "//div[contains(@class,'MuiStack-root')][.//h2[normalize-space(.)='선호 언어']]",
    "SOCIAL_ROW" :  "//h2[contains(@class,'MuiTypography-body1')][normalize-space(.)='소셜 연결 계정']",
    "LANG_ROW_ENG" :  "//div[contains(@class,'MuiStack-root')][.//h2[normalize-space(.)='language']]",
    
    "BTN_COPY_QUESTION" : "//div[@data-floating='true'])[last()]",  # 이거 해야함 
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
    "CHECK_UPLOADED_FILE" : "//*[name()='svg' and @data-testid='circle-checkIcon']",
    "FAIL_UPLOAD_FILE" : "//*[name()='svg' and @data-testid='circle-exclamationIcon']",
    "FAIL_UPLOAD_FILE_MSG" : "//p[contains(@class, 'css-wrn3u')]",
    "BTN_FOR_UPLOADED_FILE" : "//button[contains(@class, 'css-1rssx7s')]",
    "BTN_BACK_IN_MAKE_AGENT" : "//button[contains(@class, 'css-1p4tfme')]",
    "CHECK_DRAFT" : "//div[contains(@class, 'css-1alszk2')]",
    "PREVIEW_INPUT" :"//textarea[@data-gtm-form-interact-field-id = '5']",
    "BTN_PREVIEW_SEND" : "//button[contains(@class, 'css-rhb320')]",
    "BTN_PREVIEW_REFRESH" : "//div[contains(@class, 'css-16ypwk')]//button",
    "CHECK_FILE_IN_CHAT" : "//div[contains(@class, 'css-1fth50j')]",
    "CHECK_IMG_IN_CHAT" : "//img[contains(@class, 'MuiBox')]",
    
    
    
    
    # 업로드 버튼
    "BTN_UPLOAD_FILE": "//li[.//span[text()='파일 업로드']]",
    "BTN_GEN_IMAGE": "//li[.//span[text()='이미지 생성']]",
    "BTN_SEARCH_WEB": "//li[.//span[text()='웹 검색']]",
    "FILE_INPUT" : "//input[@type='file']",
    
}

