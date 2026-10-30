import os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

PPO_ID = os.environ["PPO_ID"]
EMAIL = os.environ["CONFIRM_EMAIL"]
PLATE = os.environ["PLATE"]
DAYS = os.environ.get("DAYS", "1")

opts = webdriver.ChromeOptions()
for a in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,1600"):
    opts.add_argument(a)
driver = webdriver.Chrome(options=opts)

try:
    wait = WebDriverWait(driver, 20)
    driver.get("https://vipermit.com/User/UserLogin.aspx")
    wait.until(EC.presence_of_element_located((By.ID, "txtPPOId"))).send_keys(PPO_ID)
    driver.find_element(By.XPATH, "//input[@type='submit' and @value='Continue']").click()

    wait.until(EC.presence_of_element_located((By.ID, "drpPreviousPlates")))
    Select(driver.find_element(By.ID, "drpPreviousPlates")).select_by_visible_text(PLATE)

    days = driver.find_element(By.ID, "txtDays")
    days.clear()
    days.send_keys(DAYS)

    driver.find_element(By.ID, "chkSendConfirmation").click()
    driver.find_element(By.ID, "txtEmailId").send_keys(EMAIL)
    driver.find_element(By.ID, "chkAgree").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSubmit").click()

    wait.until(lambda d: d.find_element(By.TAG_NAME, "body").text.strip() != "")
    driver.save_screenshot("result.png")
    print(f"Submitted permit: plate={PLATE}, days={DAYS}")
except Exception:
    driver.save_screenshot("error.png")
    raise
finally:
    driver.quit()
