from utils.headers import *

from pages.security_page import SecurityPage
    

    
def test_signup_security_sql_a(security_page,security_cases) :  
    security_page.go_to_signup_page()
    data = security_cases["sql_injection_a"]
    security_page.signup_email(data["sql_injection"])
    security_page.signup_pw(data["sql_injection"])
    security_page.signup_name(data["sql_injection"])
    elements = security_page.signup_checkbox()
    elements[0].click()
    security_page.btn_create()

    
#메인페이지 접속
# def test_go_to_main(logged_in_main):
#     page = logged_in_main