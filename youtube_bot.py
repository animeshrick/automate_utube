from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# LambdaTest Credentials (Replace with your details)
USERNAME = "animeshece1998"
ACCESS_KEY = "LT_QUs2XEoIOKCcncpP8VWUQXpdrHjS9oW4Qoneeypnb6QR6hW"

# Desired capabilities for Chrome on LambdaTest
capabilities = {
    "browserName": "Chrome",
    "browserVersion": "latest",
    "platformName": "Windows 10",
    "LT:Options": {
        "username": USERNAME,
        "accessKey": ACCESS_KEY,
        "resolution": "1920x1080",
        "selenium_version": "4.0.0"
    }
}

# Connect to LambdaTest Remote WebDriver
grid_url = f"https://{USERNAME}:{ACCESS_KEY}@hub.lambdatest.com/wd/hub"
driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=capabilities)

# Function to search and watch YouTube videos
def search_and_watch(query):
    driver.get("https://www.youtube.com")
    time.sleep(3)

    # Accept cookies (if shown)
    try:
        driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]").click()
    except:
        pass  # No cookie popup

    # Search for the topic
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # Click on the most watched video
    videos = driver.find_elements(By.XPATH, "//a[@id='video-title']")
    if videos:
        videos[0].click()
        time.sleep(5)  # Watch for 5 seconds

search_and_watch("Django tutorials in English")

# Close the browser
driver.quit()
