import requests
import os
import urllib.parse
from bs4 import BeautifulSoup  # To clean HTML tags

dishes = ["biryani", "dosa", "pani puri", "samosa"]  # Add your 50 dishes

def clean_filename(name):
    # Remove special characters from filenames
    return "".join(c if c.isalnum() or c in ('_', '-') else '_' for c in name)

def clean_html_tags(text):
    # Remove HTML tags from attribution using BeautifulSoup
    return BeautifulSoup(text, "html.parser").get_text() if text else "Unknown"

def download_wikimedia_images():
    os.makedirs("indian_food_images", exist_ok=True)
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    for dish in dishes:
        print(f"Searching for {dish}...")
        
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrnamespace": 6,
            "gsrsearch": f"{dish} indian food",
            "gsrlimit": 5,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata|mime"
        }
        
        response = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            
            for idx, page_id in enumerate(pages.values()):
                try:
                    image_info = page_id["imageinfo"][0]
                    img_url = image_info["url"]
                    mime_type = image_info.get("mime", "")
                    
                    # Skip non-image files (SVG/PDF/etc)
                    if not mime_type.startswith("image/"):
                        print(f"Skipping non-image file: {img_url}")
                        continue
                        
                    # Get proper file extension from URL
                    parsed_url = urllib.parse.urlparse(img_url)
                    filename = os.path.basename(parsed_url.path)
                    dish_clean = clean_filename(dish)
                    save_path = f"indian_food_images/{dish_clean}_{idx}{os.path.splitext(filename)[1]}"
                    
                    # Download image with proper headers and error handling
                    img_response = requests.get(img_url, headers=headers, stream=True)
                    img_response.raise_for_status()  # Raise an error for bad status codes
                    
                    # Check if content-type is an image
                    if 'image' not in img_response.headers.get('content-type', ''):
                        print(f"Skipping invalid image content: {img_url}")
                        continue
                    
                    # Save the image in chunks
                    with open(save_path, "wb") as f:
                        for chunk in img_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    # Clean attribution metadata
                    metadata = image_info.get("extmetadata", {})
                    author = clean_html_tags(metadata.get("Artist", {}).get("value", ""))
                    license_type = metadata.get("LicenseShortName", {}).get("value", "")
                    
                    # Save cleaned attribution
                    with open(f"{save_path}.txt", "w") as f:
                        f.write(f"Author: {author}\nLicense: {license_type}\nSource: {img_url}")
                    
                    print(f"Downloaded: {save_path}")
                    
                except Exception as e:
                    print(f"Error processing {dish}: {str(e)}")

if __name__ == "__main__":
    download_wikimedia_images()