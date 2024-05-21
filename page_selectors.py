from selenium.webdriver.common.by import By

SIGN_IN_BUTTON = (By.XPATH, "//button[contains(text(), 'Sign In')]")
SIGN_IN_WITH_GOOGLE_BUTTON = (By.XPATH, "//button[contains(., 'Sign in with Google')]")
EMAIL_INPUT = (By.ID, "identifierId")
NEXT_BUTTON = (By.XPATH, "//span[contains(text(), 'Next')]")
PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
