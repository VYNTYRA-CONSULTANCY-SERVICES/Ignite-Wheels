import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
GOOGLE_MAPS_URL = "https://maps.app.goo.gl/ciSbvABYoKvVNr1x5"
OUTPUT_FILE = "../assets/data/reviews.json"
MAX_REVIEWS = 10

def get_reviews():
    print("Launching Browser...")
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Keep headful for debugging if needed, but headless is better for background
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print(f"Navigating to {GOOGLE_MAPS_URL}...")
        driver.get(GOOGLE_MAPS_URL)
        
        # Wait for redirect and load
        time.sleep(8)
        print(f"Current URL: {driver.current_url}")
        
        # Check if we are on the right page
        if "google.com/maps" not in driver.current_url:
            print("Warning: URL does not look like Google Maps.")

        # Try to find the "Reviews" tab button
        print("Looking for Reviews tab...")
        try:
            # Look for any button with "Reviews" text
            reviews_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Reviews')]")
            if reviews_buttons:
                reviews_buttons[0].click()
                print("Clicked Reviews tab.")
                time.sleep(4)
            else:
                print("No 'Reviews' tab button found. We might be already on the reviews section or layout is different.")
        except Exception as e:
            print(f"Could not click reviews tab: {e}")

        # Scroll logic
        print("Scrolling to load reviews...")
        try:
            # Find the scrollable container. 
            # Strategy: Find the element that contains the reviews and scroll it.
            # The container usually has class 'm6QErb' and 'DxyBCb'
            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div.m6QErb.DxyBCb[role='feed']")
            
            for _ in range(3):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                time.sleep(2)
        except Exception as e:
            print(f"Scrolling failed (might be already loaded or different layout): {e}")
            # Fallback: Try scrolling the body
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Extract Reviews
        print("Extracting data...")
        
        reviews_data = []
        
        # Find all elements that look like review containers
        # Class 'jftiEf' is the standard review block class
        review_elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')
        
        print(f"Found {len(review_elements)} review elements.")

        for el in review_elements[:MAX_REVIEWS]:
            try:
                # Name: class 'd4r55'
                try:
                    name = el.find_element(By.CLASS_NAME, "d4r55").text
                except:
                    name = "Google User"

                # Rating: aria-label "X stars"
                try:
                    rating_el = el.find_element(By.CSS_SELECTOR, "span[role='img']")
                    rating_text = rating_el.get_attribute("aria-label") # "5 stars"
                    rating = float(rating_text.split(" ")[0])
                except:
                    rating = 5.0

                # Text: class 'wiI7pd'
                try:
                    text_el = el.find_element(By.CLASS_NAME, "wiI7pd")
                    text = text_el.text
                except:
                    text = ""

                # Time: class 'rsqaWe'
                try:
                    time_el = el.find_element(By.CLASS_NAME, "rsqaWe")
                    relative_time = time_el.text
                except:
                    relative_time = ""

                # Photo: class 'NBa7we' or inside button
                try:
                    img_el = el.find_element(By.CSS_SELECTOR, "button.WEBjve img")
                    photo_url = img_el.get_attribute("src")
                except:
                    photo_url = ""

                reviews_data.append({
                    "name": name,
                    "rating": rating,
                    "text": text,
                    "relative_time_description": relative_time,
                    "profile_photo_url": photo_url,
                    "location": "Google Review"
                })
                    
            except Exception as e:
                print(f"Error parsing review: {e}")
                continue

        if reviews_data:
            # Save to JSON
            script_dir = os.path.dirname(os.path.abspath(__file__))
            abs_file_path = os.path.join(script_dir, OUTPUT_FILE)
            
            with open(abs_file_path, 'w', encoding='utf-8') as f:
                json.dump(reviews_data, f, indent=4, ensure_ascii=False)
                
            print(f"Successfully saved {len(reviews_data)} reviews to {abs_file_path}")
        else:
            print("No reviews extracted.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    get_reviews()
