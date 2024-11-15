from behave import given, when, then
from selenium.webdriver.common.by import By
import logging

# utils
from utils.event_utils import WebDriverUtils

logging.basicConfig(level=logging.INFO)

setTimeOut = 10 # 定義超時時間

@given('the user is on the login page')
def step1(context):
    context.webdriver_utils = WebDriverUtils(context.driver)
    context.driver.get("http://192.168.1.247/QSERP/")
    context.driver.maximize_window()

# 登入成功測試區
@when('the user enters Username as "{username}" and Password as "{password}"')
def step2(context, username, password):
    context.webdriver_utils.set_value(By.NAME, "uid", username)
    context.webdriver_utils.set_value(By.NAME, "pwd", password)
    context.driver.find_element(By.TAG_NAME, "form").submit()

@then('the user should be logged in successfully')
def step3_1(context):
    try:
        ifHomePage = context.webdriver_utils.wait_for_url_contains("http://192.168.1.247/servlet/jform#")
        logging.info(f"Home page check result: {ifHomePage}")
        
        # 斷言 非預期結果        
        # 正常帳密卻登入錯誤
        assert ifHomePage, "Test failed. Login failed."

        # 登出
        if ifHomePage:
            context.webdriver_utils.click_element(By.XPATH, "//div[@id='path']/span[2]/div")
            context.webdriver_utils.click_element(By.ID, "logout")
            print('登出')
        
        
    except Exception as e:
        # 如果登入失敗，檢查 URL 是否包含登入頁面的 URL
        try:
            # http://192.168.1.247/servlet/jform 紅色
            # http://210.61.91.56:8001/servlet/jform?file=QSERP.dat 重新登入
            page = context.webdriver_utils.wait_for_url_contains('http://210.61.91.56:8001/servlet/jform?file=QSERP.dat') 
            assert not page, f"Login failed. Open 重新登入頁 - http://210.61.91.56:8001/servlet/jform?file=QSERP.dat : {e}"
        except Exception as inner_exception:            
            logging.error(f"Error occurred: {inner_exception}")
            raise AssertionError(f"Login failed. Unable to verify page: {inner_exception}")

@then('the user should be redirected to the login page')
def step3_2(context):
    try:           
        ifLoginPage = context.webdriver_utils.wait_for_element(By.NAME, "uid")
        logging.info(f"Login page check result: {ifLoginPage}")

        # 斷言 非預期結果        
        # 若不是回登入頁
        assert ifLoginPage, "Test failed. The user not redirected to the login page"

    except Exception as e:
        try:
            ifHomePage = context.webdriver_utils.wait_for_url_contains("http://192.168.1.247/servlet/jform#")
            assert not ifHomePage, f"Test failed. Wrong user but login successfully: {e}"
        except Exception as inner_exception:
            logging.error(f"Error occurred: {inner_exception}")
            raise AssertionError(f"Failed to redirect to login page or incorrect behavior detected: {inner_exception}")