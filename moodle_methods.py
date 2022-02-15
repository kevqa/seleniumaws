import unittest
import datetime
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
s = Service(executable_path='./chromedriver')
import moodle_locators as locators

from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

#----------------------------------------------------------------------------------------------------------------------#

# Fixture method - to open web browser
def setUp():
    # Make a full screen
    driver.maximize_window()

    # Let's wait for browser response in general
    driver.implicitly_wait(30)

    # Navigating to the Moodle app website
    driver.get(locators.moodle_url)

    # Checking that we're on the correct URL address and we are seeing the correct title
    if driver.current_url == locators.moodle_url and driver.title == 'Software Quality Assurance Testing':
        print(f'We are at the Moodle homepage -- {driver.current_url}')
        print(f'We\'re seeing the title message -- "Software Quality Assurance Testing"')
        #sleep(4)
        #driver.close()
    else:
        print(f'We are not at the moodle homepage, check your code.')
        driver.close()
        driver.quit()

def tearDown():
    if driver is not None:
        print(f'------------------------------')
        print(f'Test Completed at: {datetime.datetime.now()}')
        driver.close()
        driver.quit()
        # Make a log file
        old_instance = sys.stdout
        log_file = open('message log', 'w')
        sys.stdout = log_file
        print(f'Email {locators.email} \nUsername: {locators.new_username} \nPassword: {locators.new_password}')
        sys.stdout = old_instance
        log_file.close()

def log_in(username, password):
    if driver.current_url == locators.moodle_url:
        driver.find_element(By.LINK_TEXT, 'Log in').click()
        if driver.current_url == locators.moodle_login_url:
            driver.find_element(By.ID, 'username').send_keys(username)
            sleep(0.25)
            driver.find_element(By.ID, 'password').send_keys(password)
            sleep(0.25)
            driver.find_element(By.ID, 'loginbtn').click()
            if driver.title == 'Dashboard':
                assert driver.current_url == locators.moodle_dashboard
                print(f'Log in successful. Dashboard is present.\n '
                      f'We logged in with Username {username} and Password {password}')
            else:
                print(f'Total fail my broski! TAKE 2!')

def log_out():
    driver.find_element(By.CLASS_NAME, 'userpicture').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//span[contains(., "Log out")]').click()
    sleep(0.25)
    if driver.current_url == locators.moodle_url:
        print(f'I must go. My people need me!: {datetime.datetime.now()}')

#----------------------------------------------------------------------------------------------------------------------#

def create_new_user():
    driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    assert driver.find_element(By.LINK_TEXT, 'Users').is_displayed()
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Add a new user').click()
    sleep(0.25)
    assert driver.find_element(By.LINK_TEXT, 'Add a new user').is_displayed()
    sleep(0.25)
    #enter fake data into username open field
    driver.find_element(By.ID, 'id_username').send_keys(locators.new_username)
    print(locators.new_username)
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Click to enter text').click()
    sleep(0.25)
    driver.find_element(By.ID, 'id_newpassword').send_keys(locators.new_password)
    sleep(0.25)
    driver.find_element(By.ID, 'id_firstname').send_keys(locators.first_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_lastname').send_keys(locators.last_name)
    sleep(0.25)
    driver.find_element(By.ID, 'id_email').send_keys(locators.email)

    # Select 'Allow everyone to see my email address'
    Select(driver.find_element(By.ID, 'id_maildisplay')).select_by_visible_text('Allow everyone to see my email address')
    sleep(0.25)
    driver.find_element(By.ID, 'id_moodlenetprofile').send_keys(locators.moodle_net_profile)
    sleep(0.25)
    driver.find_element(By.ID, 'id_city').send_keys(locators.city)
    sleep(0.25)
    Select(driver.find_element(By.ID, 'id_country')).select_by_visible_text('Canada')
    sleep(0.25)
    Select(driver.find_element(By.ID, 'id_timezone')).select_by_visible_text('America/Vancouver')
    sleep(0.25)
    driver.find_element(By.ID, 'id_description_editoreditable').clear()
    sleep(0.25)
    driver.find_element(By. ID, 'id_description_editoreditable').send_keys(locators.description)
    sleep(0.25)

    # Upload picture to the user picture section
    # Click by 'You can drag and drop files here to add them.' section
    driver.find_element(By. CLASS_NAME, 'dndupload-arrow').click()
    sleep(1)
    driver.find_element(By. PARTIAL_LINK_TEXT, 'Server files').click()
    sleep(1)
    driver.find_element(By. PARTIAL_LINK_TEXT, 'Cosmetics').click()
    sleep(1)
    driver.find_element(By. PARTIAL_LINK_TEXT, 'Biotherm 2021 fall school').click()
    sleep(1)
    driver.find_element(By. PARTIAL_LINK_TEXT, 'Course image').click()
    sleep(1)
    driver.find_element(By. PARTIAL_LINK_TEXT, 'BT2021fall.png').click()
    sleep(1)
    # Click by 'Select this file' button
    driver.find_element(By. XPATH, '//button[contains(., "Select this file")]').click()
    sleep(0.25)
    # Enter value to the picture 'description' open field
    driver.find_element(By. ID, 'id_imagealt').send_keys(locators.pic_desc)
    sleep(0.25)
    # Click by 'Additional name' drop down menu
    driver.find_element(By.XPATH, '//a[contains(., "Additional names")]').click()
    sleep(0.25)
    driver.find_element(By. ID, 'id_firstnamephonetic').send_keys(locators.phonetic_name)
    sleep(0.25)
    driver.find_element(By. ID, 'id_lastnamephonetic').send_keys(locators.phonetic_name)
    sleep(0.25)
    driver.find_element(By. ID, 'id_middlename').send_keys(locators.phonetic_name)
    sleep(0.25)
    driver.find_element(By. ID, 'id_alternatename').send_keys(locators.phonetic_name)
    sleep(0.25)
    # Click by 'Interests' drop down menu
    driver.find_element(By.XPATH, '//a[contains(., "Interests")]').click()
    sleep(0.25)
    # Using for loop, take all items from the list and populate data
    for tag in locators.list_of_interests:
        driver.find_element(By. XPATH, '//div[3]/input').click()
        sleep(0.25)
        driver.find_element(By.XPATH, '//div[3]/input').send_keys(tag)
        sleep(0.25)
        driver.find_element(By.XPATH, '//div[3]/input').send_keys(Keys.ENTER)
    sleep(0.25)

    # Fill Optional section
    # Click by Optional link to open that section
    driver.find_element(By.XPATH, "//a[text() = 'Optional']").click()
    sleep(0.25)
    # Fill out the Web page input field
    driver.find_element(By.CSS_SELECTOR, "input#id_url").send_keys(locators.web_page_url)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_icq").send_keys(locators.icq_number)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_skype").send_keys(locators.new_username)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_aim").send_keys(locators.new_username)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_yahoo").send_keys(locators.new_username)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_msn").send_keys(locators.new_username)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_idnumber").send_keys(locators.icq_number)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_institution").send_keys(locators.institution)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_department").send_keys(locators.department)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_phone1").send_keys(locators.phone)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_phone2").send_keys(locators.mobile_phone)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, "input#id_address").send_keys(locators.address)
    sleep(0.25)
    # Click by 'Create user' button
    driver.find_element(By.ID, 'id_submitbutton').click()
    sleep(1)
    print(f'--- Test Scenario: Create a new user {locators.new_username} --- passed')

def check_user_created():
    if driver.current_url == locators.moodle_users_main_page:
        assert driver.find_element(By.XPATH, "//h1[text() = 'Software Quality Assurance Testing']").is_displayed()
        if driver.find_element(By.ID, 'fgroup_id_email_grp_label') and \
            driver.find_element(By.NAME, 'email'):
            sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, 'input#id_email').send_keys(locators.email)
            sleep(0.25)
            driver.find_element(By.CSS_SELECTOR, 'input#id_addfilter').click()
            sleep(0.25)
            if driver.find_element(By.XPATH, f'//td[contains(., "{locators.email}")]'):
                print('--- Test Scenario: Check user created --- passed')
                log_out()

def check_we_logged_in_with_new_cred():
    if driver.current_url == locators.moodle_dashboard:
        if driver.find_element(By.XPATH, f'//span[contains(., "{locators.full_name}")]').is_displayed():
            print(f'--- User with the name {locators.full_name} is displayed. Test Passed ---')
            log_out()

def delete_user():
    driver.find_element(By.XPATH, '//span[contains(., "Site administration")]').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Users').click()
    sleep(0.25)
    driver.find_element(By.LINK_TEXT, 'Browse list of users').click()
    sleep(0.25)
    if driver.current_url == locators.moodle_users_main_page:
        print(f'Back to the User page. {locators.moodle_users_main_page}')
    else:
        print(f'Error detected. Examine code.')
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, 'input#id_email').send_keys(locators.email)
    sleep(0.25)
    driver.find_element(By.CSS_SELECTOR, 'input#id_addfilter').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/section/div/div[1]/table/tbody/tr/td[6]/a[1]/i').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//button[contains(.,"Delete")]').click()
    sleep(0.25)
    print(f'User has been deleted.')

#----------------------------------------------------------------------------------------------------------------------#
setUp()
log_in(locators.moodle_username, locators.moodle_password)
create_new_user()
check_user_created()

#Checking the New User Credentials
setUp()
log_in(locators.new_username, locators.new_password)
check_we_logged_in_with_new_cred()
log_in(locators.moodle_username, locators.moodle_password)
delete_user()
log_out()
tearDown()