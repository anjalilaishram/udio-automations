import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import DEFAULT_TIMEOUT_SECONDS, DEFAULT_EMAIL, DEFAULT_PASSWORD
from page_selectors import SIGN_IN_BUTTON, SIGN_IN_WITH_GOOGLE_BUTTON, EMAIL_INPUT, NEXT_BUTTON, PASSWORD_INPUT

def init_driver():
    return uc.Chrome(headless=False)

def open_webpage(driver, url):
    driver.get(url)

def click_button(driver, by, value):
    button = WebDriverWait(driver, DEFAULT_TIMEOUT_SECONDS).until(
        EC.visibility_of_element_located((by, value))
    )
    button.click()

def wait_for_element(driver, by, value):
    WebDriverWait(driver, DEFAULT_TIMEOUT_SECONDS).until(
        EC.visibility_of_element_located((by, value))
    )

def enter_text(driver, by, value, text):
    input_field = driver.find_element(by, value)
    input_field.send_keys(text)

def get_cookies(driver):
    return driver.get_cookies()

def construct_cookies_header(driver):
    cookies = get_cookies(driver)
    cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    return cookie_header

def login(url, email, password):
    driver = init_driver()
    try:
        open_webpage(driver, url)
        
        click_button(driver, *SIGN_IN_BUTTON)
        click_button(driver, *SIGN_IN_WITH_GOOGLE_BUTTON)

        wait_for_element(driver, *EMAIL_INPUT)
        enter_text(driver, *EMAIL_INPUT, DEFAULT_EMAIL)

        click_button(driver, *NEXT_BUTTON)
        wait_for_element(driver, *PASSWORD_INPUT)
        enter_text(driver, *PASSWORD_INPUT, DEFAULT_PASSWORD)

        click_button(driver, *NEXT_BUTTON)
        input("Press Enter to continue...")

        return driver
    finally:
        driver.quit()

if __name__ == "__main__":
    driver = login('https://www.udio.com/', DEFAULT_EMAIL, DEFAULT_PASSWORD)
    
    
