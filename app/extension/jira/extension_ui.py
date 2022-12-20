import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login

from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    # @print_timing("selenium_app_custom_action")
    # def measure():
    #     @print_timing("selenium_app_custom_action:view_issue")
    #     def sub_measure():
    #         page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
    #         page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
    #         page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
    #     sub_measure()
    # measure()

    @print_timing("selenium_ideal_forms)")
    def measure():
        @print_timing("selenium_ideal_forms:load_iforms_admin")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?decorator=admin")
            WebDriverWait(webdriver, 10).until(EC.text_to_be_present_in_element(
                                (By.XPATH, "//*[@id=\"main\"]/div/table[1]/tbody/tr/td[2]"), "Ideal Forms for JIRA")
                            )
        sub_measure()

        @print_timing("selenium_ideal_forms:load_iforms_admin")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?ijfAction=getConfig&version=0")
            WebDriverWait(webdriver, 10).until(EC.text_to_be_present_in_element(
                                (By.XPATH, "/html/body"), "forms")
                            )
        sub_measure()

        @print_timing("selenium_ideal_forms:list_issues_form")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?formId=GPE%20List")
            page.wait_until_visible((By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div"))
        sub_measure()

        @print_timing("selenium_ideal_forms:double_click_open_from_list")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?formId=GPE%20List")
            page.wait_until_visible((By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div"))
            div = webdriver.find_element(By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div")
            actionChains = ActionChains(webdriver)
            actionChains.double_click(div).perform()

            current_url = webdriver.current_url
            WebDriverWait(webdriver, 15).until(EC.url_changes(current_url))
            new_url = webdriver.current_url
            print(new_url)
        sub_measure()


        @print_timing("selenium_ideal_forms:create_new_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?formId=GPE%20List")
            page.wait_until_visible((By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div"))
            button = webdriver.find_element(By.XPATH, "//*[@id=\"ijfContent_ctr_d_1_6_5\"]/div/button")
            actionChains = ActionChains(webdriver)
            actionChains.click(button).perform()

            #current_url = webdriver.current_url
            #WebDriverWait(webdriver, 15).until(EC.url_changes(current_url))

            page.wait_until_visible((By.XPATH, "//*[@id=\"ijfContent_ctr_3_3-inputEl\"]"))

            summary_field = webdriver.find_element(By.XPATH, "//*[@id=\"ijfContent_ctr_3_3-inputEl\"]")
            summary_field.send_keys("New Item Test Summary")

            description_field = webdriver.find_element(By.XPATH, "//*[@id=\"ijfContent_ctr_10_3\"]")
            description_field.send_keys("New Item Test Description")

            save_button = webdriver.find_element(By.XPATH, "//*[@id='ijfContent_11_4']/div/button[1]/span[1]")
            save_button.click()

            current_url = webdriver.current_url
            WebDriverWait(webdriver, 15).until(EC.url_changes(current_url))
            try:
                WebDriverWait(webdriver, 1).until(EC.alert_is_present())
                webdriver.switch_to.alert.accept()
            except Exception:
                print("no alert box")
        sub_measure()

        @print_timing("selenium_ideal_forms:update_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/iforms?formId=GPE%20List")
            page.wait_until_visible((By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div"))
            div = webdriver.find_element(By.XPATH, "//div[@class='x-grid-item-container']//table[1]//td[1]/div")
            actionChains = ActionChains(webdriver)
            actionChains.double_click(div).perform()

            current_url = webdriver.current_url
            WebDriverWait(webdriver, 15).until(EC.url_changes(current_url))

            page.wait_until_visible((By.XPATH, "//*[@id='ijfContent_ctr_3_3-inputEl']"))

            title_text_elem = webdriver.find_element(By.XPATH, "//*[@id='ijfContent_ctr_d_1_1_2']/div/div/span")
            #title_text = title_text_elem.get_attribute("value")

            summary_field = webdriver.find_element(By.XPATH, "//*[@id='ijfContent_ctr_3_3-inputEl']")
            summary_field.clear()
            summary_field.send_keys("Update Issue Test ")
            summary_field.send_keys(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

            save_button = webdriver.find_element(By.XPATH, "//*[@id='ijfContent_11_4']/div/button[1]/span[1]")
            save_button.click()

            #webdriver.implicitly_wait(15)
            WebDriverWait(webdriver, 10).until(EC.text_to_be_present_in_element(
                    (By.XPATH, "//*[@id='ijfContent_ctr_d_1_1_2']/div/div/span"), summary_field.text)
                )
            #webdriver.switch_to.alert.accept()

            #current_url = webdriver.current_url
            #WebDriverWait(webdriver, 15).until(EC.url_changes(current_url))
            #actionChains.click(save_button).perform()
            try:
                WebDriverWait(webdriver, 1).until(EC.alert_is_present())
                webdriver.switch_to.alert.accept()
            except Exception:
                print("no alert box")
        sub_measure()

    measure()


