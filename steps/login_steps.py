from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO)

setTimeOut = 10 # 定義超時時間

# 等待元素
def wait_for_element(context, by, value, timeout=setTimeOut):
    return WebDriverWait(context.driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

# 等待 URL
def wait_for_url_contains(context, url_string, timeout=setTimeOut):
    return WebDriverWait(context.driver, timeout).until(
        EC.url_contains(url_string)
    )

@given('the user is on the login page')
def step_impl(context):
    context.driver.get("http://192.168.1.247/QSERP/")
    context.driver.maximize_window()

# 登入成功測試區
@when('the user enters Username as "{username}" and Password as "{password}"')
def step_impl(context, username, password):
    username_field = wait_for_element(context, By.NAME, "uid")
    password_field = context.driver.find_element(By.NAME, "pwd")
    
    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    context.driver.find_element(By.TAG_NAME, "form").submit()

@then('the user should be logged in successfully')
def step_impl(context):
    try:
        ifHomePage = wait_for_url_contains(context, "http://192.168.1.247/servlet/jform#")
        logging.info(f"Home page check result: {ifHomePage}")
        
        # 斷言 非預期結果        
        # 正常帳密卻登入錯誤
        assert ifHomePage, "Test failed. Login failed."

        # 登出
        if ifHomePage:
            button3  = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='path']/span[2]/div")))
            button3.click()        
            button4 = context.driver.find_element(By.ID, "logout")
            button4.click()
            print('登出')
        
        
    except Exception as e:
        # 如果登入失敗，檢查 URL 是否包含登入頁面的 URL
        try:
            # http://192.168.1.247/servlet/jform 紅色
            # http://210.61.91.56:8001/servlet/jform?file=QSERP.dat 重新登入
            page = wait_for_url_contains(context, 'http://210.61.91.56:8001/servlet/jform?file=QSERP.dat') 
            assert not page, f"Login failed. Open 重新登入頁 - http://210.61.91.56:8001/servlet/jform?file=QSERP.dat : {e}"
        except Exception as inner_exception:            
            logging.error(f"Error occurred: {inner_exception}")
            raise AssertionError(f"Login failed. Unable to verify page: {inner_exception}")

@then('the user should be redirected to the login page')
def step_impl(context):
    try:           
        ifLoginPage = wait_for_element(context, By.NAME, "uid")
        logging.info(f"Login page check result: {ifLoginPage}")

        # 斷言 非預期結果        
        # 若不是回登入頁
        assert ifLoginPage, "Test failed. The user not redirected to the login page"

    except Exception as e:
        try:
            ifHomePage = wait_for_url_contains(context, "http://192.168.1.247/servlet/jform#")
            assert not ifHomePage, f"Test failed. Wrong user but login successfully: {e}"
        except Exception as inner_exception:
            logging.error(f"Error occurred: {inner_exception}")
            raise AssertionError(f"Failed to redirect to login page or incorrect behavior detected: {inner_exception}")