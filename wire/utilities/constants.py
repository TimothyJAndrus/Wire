from selenium.webdriver.common.by import By

IDENTIFIERS = {
    "#": By.ID,
    "@": By.NAME,
    "*": By.XPATH,
    "~": By.TAG_NAME,
    ".": By.CLASS_NAME,
    "_": By.CSS_SELECTOR,
}
