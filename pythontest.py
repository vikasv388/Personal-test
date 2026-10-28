from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("https://www.google.com")
driver.maximize_window()

# Search field locate karo
search_box = driver.find_element(By.NAME, "q")

# Check search field
if search_box.is_displayed() and search_box.is_enabled():
    print("Search field is visible and enabled")
else:
    print("Search field is NOT working")

# Search text enter karo
search_box.send_keys("SQL automation testing")

# Search perform karo
search_box.send_keys(Keys.ENTER)

time.sleep(3)

print("Search completed successfully")

driver.quit()
