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
        self.driver.get(url)

        # 執行 JavaScript 來取得頁面加載的性能指標
        performance = self.driver.execute_script("return window.performance.timing")
        # 從 performance 對象中計算頁面加載時間
        navigation_start = performance['navigationStart']
        load_event_end = performance['loadEventEnd']

        load_time = (load_event_end - navigation_start) / 1000  # 轉換成秒
        # if(load_time > 5):            
        #     
        print(f"頁面加載時間: {load_time} 秒")

        self.driver.maximize_window()
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
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # 打開新標籤頁並切換
        self.driver.execute_script(f"window.open('{qs['page']}')")
        self.driver.close()          
        self.driver.switch_to.window(self.Driver.window_handles[-1])
        logging.info(f"已切換到新頁面: {qs['page']}")

        # connectStart: 與伺服器建立連接的開始時間。
        # connectEnd: 與伺服器建立連接的結束時間。

    def get_page_load_time(self):
        # 計算頁面加載時間
        try:
            # 執行 JavaScript 來取得頁面加載的性能指標
            performance = self.driver.execute_script("return window.performance.timing")

            # 從 performance 對象中計算頁面加載時間
            navigation_start = performance['navigationStart']
            load_event_end = performance['loadEventEnd']

            load_time = (load_event_end - navigation_start) / 1000  # 轉換成秒
            print(f"耗時 : {load_time}")
            return load_time
        except Exception as e:
            logging.error(f"Error occurred while calculating page load time: {e}")
            return 0  # 如果計算失敗，返回 0 作為頁面加載時間

# 假設我們的 WebDriverUtils 已經正確設置了
class BugReportPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_bug_report_page(self, url):
        self.driver.get(url)
        logging.info(f"已打開頁面: {url}")

    def enter_report_text(self, report_text):
        # 假設報告文本框是通過 name 定位
        report_text_area = self.driver.find_element(By.NAME, 'reportText')
        report_text_area.clear()
        report_text_area.send_keys(report_text)
        logging.info(f"已輸入 Bug 描述: {report_text}")

    def attach_file(self, file_path):
        # 假設上傳檔案的 input 元素是通過 name 定位
        file_input = self.driver.find_element(By.NAME, 'fileInput')
        file_input.send_keys(file_path)
        logging.info(f"已附加檔案: {file_path}")

    def submit_report(self):
        # 假設送出按鈕是通過 id 定位
        submit_button = self.driver.find_element(By.ID, 'submitReport')
        submit_button.click()
        logging.info("已送出 Bug 回報")

    def verify_submission(self):
        # 等待回報送出後顯示成功訊息
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'successMessage'))
        )
        success_message = self.driver.find_element(By.ID, 'successMessage')
        return "Bug report submitted successfully" in success_message.text