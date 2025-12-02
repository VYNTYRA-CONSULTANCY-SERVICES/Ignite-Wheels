import requests
import json
import os
import time

# --- CONFIGURATION ---
# 1. Get your API Key from Google Cloud Console (enable Places API)
API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"

# 2. Get your Place ID from: https://developers.google.com/maps/documentation/places/web-service/place-id
# Search for "Ignite Wheels Srikakulam"
PLACE_ID = "YOUR_PLACE_ID_HERE" 

# Path to your JSON database
JSON_DB_PATH = "assets/data/reviews.json"

def fetch_google_reviews():
    print("Fetching reviews from Google Maps...")
    
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={PLACE_ID}&fields=reviews&key={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "result" in data and "reviews" in data["result"]:
            google_reviews = data["result"]["reviews"]
            print(f"Found {len(google_reviews)} reviews on Google.")
            return google_reviews
        else:
            print("No reviews found or API Error:", data.get("status", "Unknown Error"))
            return []
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def update_json_database(new_reviews):
    # 1. Load existing reviews
    if os.path.exists(JSON_DB_PATH):
        with open(JSON_DB_PATH, "r", encoding="utf-8") as f:
            try:
                existing_reviews = json.load(f)
            except json.JSONDecodeError:
                existing_reviews = []
    else:
        existing_reviews = []

    # 2. Convert Google Reviews to our format
    formatted_reviews = []
    for review in new_reviews:
        formatted_reviews.append({
            "name": review.get("author_name", "Anonymous"),
            "location": "Google User", # Google doesn't give location usually
            "rating": review.get("rating", 5),
            "text": review.get("text", ""),
            "source": "google", # Mark as google source
            "time": review.get("time", 0) # Unix timestamp to help with sorting/deduplication
        })

    # 3. Merge and Deduplicate
    # We use (name + text) as a unique key to avoid duplicates
    existing_keys = { (r["name"] + r["text"]) for r in existing_reviews }
    
    added_count = 0
    for r in formatted_reviews:
        key = r["name"] + r["text"]
        if key not in existing_keys:
            existing_reviews.append(r)
            existing_keys.add(key)
            added_count += 1
            
    # 4. Save back to file
    with open(JSON_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_reviews, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully added {added_count} new reviews to {JSON_DB_PATH}")

if __name__ == "__main__":
    if API_KEY == "YOUR_GOOGLE_PLACES_API_KEY":
        print("ERROR: Please set your API_KEY and PLACE_ID in the script first!")
    else:
        reviews = fetch_google_reviews()
        if reviews:
            update_json_database(reviews)
