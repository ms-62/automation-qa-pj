from utils.headers import *

from pages import (
    signup_page,
    login_page,
    main_page,
    member_page,
    security_page
) 
    
def test_signup_security(signup_page) :  
    signup_page.go_to_signup_page()
    sql_cases = security_cases["sql_injection"]
    for case in sql_cases:
        data = case["value"]
        signup_page.signup_email(data)
        signup_page.signup_pw(data)
        signup_page.signup_name(data)
    elements = signup_page.signup_checkbox()
    elements[0].click()
    signup_page.btn_create()
    
    print("PHC-TS02-TC001 : Test success")
    
#메인페이지 접속
# def test_go_to_main(logged_in_main):
#     page = logged_in_main