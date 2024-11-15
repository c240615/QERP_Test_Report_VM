from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(level=logging.INFO)

class WebDriverUtils:
    def __init__(self, driver, timeout=10):  
        self.driver = driver
        self.Actions = ActionChains(driver)
        self.timeout = timeout

    def OpenUrl(self, url):
        # 打開指定的 URL 並最大化瀏覽器窗口
        self.Driver.get(url)
        self.Driver.maximize_window()
        logging.info(f"已打開 URL: {url}")

    def wait_for_element(self, by, selector):        
        try:
            # 等待元素
            return WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, selector))
            )
        except TimeoutException as e:            
            logging.error(f"元素 {selector} 超時: {e}")
            raise

    def wait_for_url_contains(self, url_string):       
        try:
            # 等待 URL
            return WebDriverWait(self.driver, self.timeout).until(
                EC.url_contains(url_string)
            )
        except TimeoutException as e:
            logging.error(f"URL {url_string} 超時: {e}")
            raise

    # 滑鼠事件
    def click_element(self, by, selector):        
        element = self.wait_for_element(by, selector)
        if element:
            self.Actions.click(element).perform()
            logging.info(f"已點擊元素: {selector}")
        else:
            logging.warning(f"未找到元素 {selector} ")   
    
    # 鍵盤事件
    def set_value(self, by, selector, text):
        # 在指定元素中輸入
        element = self.wait_for_element(by, selector)
        if element:
            element.clear()
            element.send_keys(text, Keys.RETURN)
            logging.info(f"已在元素 {selector} 中輸入 '{text}'")
        else:
            logging.warning(f"未找到元素 {selector} ，無法輸入。")

    def get_value(self, by, selector):
        # 獲取指定元素的值
        element = self.wait_for_element(by, selector)
        if element:
            return element.text
        else:
            logging.warning(f"未找到元素 {selector}")

    def login(self, qs):
        # 執行登入操作
        self.OpenUrl(qs['link'])

        # 登入
        self.set_value(By.NAME, "uid", qs['empId'])
        self.set_value(By.NAME, "pwd", qs['password'])
        self.Driver.find_element(By.TAG_NAME, "form").submit()

        # 打開新標籤頁並切換
        self.Driver.execute_script(f"window.open('{qs['page']}')")
        self.Driver.close()          
        self.Driver.switch_to.window(self.Driver.window_handles[-1])
        logging.info(f"已切換到新頁面: {qs['page']}")