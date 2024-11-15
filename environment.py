from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    # 測試開始前初始化 WebDriver    
    context.driver = webdriver.Chrome()  # ChromeDriverManager().install()
    context.driver.maximize_window()

def after_all(context):
    if hasattr(context, 'driver'):
        context.driver.quit()