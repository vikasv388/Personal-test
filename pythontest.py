
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start Chrome browser
driver = webdriver.Chrome()

try:
    # Open website
    driver.get("https://www.google.com")

    # Maximize browser
    driver.maximize_window()

    # Test 1: Verify page title
    assert "Google" in driver.title
    print("PASS: Page title verified")

    # Test 2: Find search box
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "q"))
    )
    print("PASS: Search box found")

    # Test 3: Enter search text
    search_box.send_keys("Python Selenium testing")
    search_box.send_keys(Keys.ENTER)

    # Test 4: Verify search results page
    WebDriverWait(driver, 10).until(
        EC.url_contains("search")
    )
    print("PASS: Search submitted successfully")

except Exception as error:
    print("FAIL:", error)

finally:
    # Close browser
    driver.quit()
