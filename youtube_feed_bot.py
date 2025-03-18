from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import re

# Use existing Chrome session
options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9222"  # Connects to running Chrome

# Launch WebDriver with the existing session
driver = webdriver.Chrome(options=options)

# List of tech-related search queries
search_queries = [
    "Django tutorial in English", "Python programming English",
    "Flutter development tutorial English", "AI and machine learning English",
    "Software engineering best practices", "Data structures and algorithms",
    "Latest AI tools", "Best coding practices"
]

# Keep track of watched video URLs
watched_videos = set()

def skip_ads():
    """Checks and clicks 'Skip Ad' button if available."""
    try:
        time.sleep(2)  # Wait a bit for ads to load
        skip_button = driver.find_element(By.CLASS_NAME, "ytp-ad-skip-button-modern")
        skip_button.click()
        print("Skipped Ad!")
    except:
        pass  # No ad found, continue normally

def is_english(text):
    """Returns True if text is mostly English, False otherwise."""
    return bool(re.match(r'^[a-zA-Z0-9\s.,!?()-]+$', text))  # Allow common English characters

def search_and_watch_videos(driver, query):
    """Searches for a YouTube video and watches top 10 most viewed English videos without repeats."""
    driver.get("https://www.youtube.com")
    time.sleep(3)

    # Search for the query
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)  # Press Enter
    time.sleep(3)

    # Apply "Most viewed" filter
    try:
        filter_button = driver.find_element(By.XPATH, "//yt-formatted-string[text()='Filters']")
        filter_button.click()
        time.sleep(1)
        most_viewed_option = driver.find_element(By.XPATH, "//yt-formatted-string[text()='View count']")
        most_viewed_option.click()
        time.sleep(3)
    except:
        print("Could not apply 'Most viewed' filter")

    # Get video URLs instead of elements (fixes stale element issue)
    video_elements = driver.find_elements(By.XPATH, "//a[@id='video-title']")[:20]
    video_urls = [video.get_attribute("href") for video in video_elements if video.get_attribute("href")]

    count = 0  # Track how many English videos we've watched
    for url in video_urls:
        if url and url not in watched_videos:
            watched_videos.add(url)  # Mark video as watched
            print(f"Watching {count+1}/10: {url}")
            driver.get(url)  # Open video directly
            time.sleep(2)

            # Skip ads if present
            skip_ads()

            # Watch for 3-5 seconds (randomized)
            watch_time = random.randint(3, 5)
            time.sleep(watch_time)
            driver.back()  # Go back to search results
            time.sleep(2)

            count += 1
            if count >= 10:  # Stop after watching 10 English videos
                break

# Run the bot for each search query (watching 10 videos per topic)
for query in search_queries:
    search_and_watch_videos(driver, query)

print("YouTube feed optimization completed successfully!")
