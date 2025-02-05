from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(options=options)

def load_all_comments():
    """Scroll within the comment section to load all comments."""
    try:
        # Wait for the comment section to load
        comment_section = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x9f619') and contains(@class, 'x1n2onr6')]"))
        )

        # Click "View more comments" if it exists
        while True:
            try:
                view_more_button = WebDriverWait(comment_section, 5).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[@role='button' and contains(., 'View more comments')]"))
                )
                driver.execute_script("arguments[0].click();", view_more_button)
                time.sleep(2)
            except:
                break  # Exit if no more "View more comments" buttons

        # Scroll inside the comment section to load all comments
        last_height = 0
        while True:
            # Scroll to the bottom of the comment section
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_section)
            time.sleep(3)  # Wait for comments to load

            # Check if new comments were loaded
            new_height = driver.execute_script("return arguments[0].scrollHeight", comment_section)
            if new_height == last_height:
                break
            last_height = new_height

    except Exception as e:
        print("Error loading comments:", e)

try:
    # Open Facebook video URL
    driver.get("https://www.facebook.com/photo/?fbid=1129572312294282&set=a.759281365990047")
    
    # Wait for manual login
    input("Log in manually and press Enter to continue...")

    # Wait for the page to load
    time.sleep(5)

    # Load all comments
    load_all_comments()

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract comments (updated selectors)
    comments = []
    comment_blocks = soup.select("div.x1lliihq.xjkvuk6.x1iorvi4")  # Updated selector for comments
    for block in comment_blocks:
        author = block.select_one("strong span")  # Author name
        comment_text = block.select_one("div.xdj266r")  # Comment text
        timestamp = block.select_one("abbr")  # Timestamp
        
        comments.append({
            "Author": author.text if author else "N/A",
            "Comment": comment_text.text if comment_text else "",
            "Timestamp": timestamp["data-utime"] if timestamp else ""
        })

    # Save to Excel
    df = pd.DataFrame(comments)
    df.to_excel("653736960558242.xlsx", index=False)
    print(f"Saved {len(comments)} comments!")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()