from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time



from behave import given, when, then

@given('user is on a page with QERP-BUG and version button')
def step_given(context):
    context.driver.get('http://your-website.com')  # 使用真實的 URL
    logging.info("User is on the Bug Report page with QERP-BUG and version button.")

@when('user submit reportText as "{reportText}" and file as "{file}"')
def step_when(context, reportText, file):
    context.bug_report_page = BugReportPage(context.driver)
    context.bug_report_page.enter_report_text(reportText)
    context.bug_report_page.attach_file(file)
    context.bug_report_page.submit_report()

@then('sent report successfully')
def step_then(context):
    assert context.bug_report_page.verify_submission(), "Bug report was not submitted successfully"
    logging.info("Bug report was submitted successfully.")
