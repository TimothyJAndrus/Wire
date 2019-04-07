from selenium.webdriver.common.by import By

identifier_table = {
    "#": By.ID,
    "@": By.NAME,
    "*": By.XPATH,
    "~": By.TAG_NAME,
    ".": By.CLASS_NAME,
    "_": By.CSS_SELECTOR,
}
