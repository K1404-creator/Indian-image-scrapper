import os
import requests
import urllib.parse
import time
from typing import List, Dict

# List of Indian dresses
dresses = ["Saree", "Lehenga", "Salwar Kameez", "Anarkali",
    "Kurta", "Dhoti", "Sherwani", "Churidar",
    "Punjabi Suit", "Kurti", "Nehru Jacket", "Wedding Lehenga",   "Indian Bridal Lehenga", 
    "Traditional Silk Saree",
    "Designer Anarkali Suit",
    "Wedding Sharara",
    "Patiala Salwar Suit",
    "Designer Saree",
    "Bridal Gharara",
    "Festival Lehenga",
    "Party Wear Saree",
    "Wedding Gown India",
    "Designer Kurti",
    "Bollywood Lehenga",  # Festival Wear
    "Diwali Silk Saree",
    "Garba Chaniya Choli",
    "Eid Sharara Suit",
    "Holi Special Kurta",
    
    # Wedding Collection
    "Heavy Bridal Lehenga",
    "Designer Wedding Saree",
    "Marriage Sherwani",
    "Indian Bridal Gown",
    
    # Regional Fashion
    "South Indian Silk Saree",
    "Punjabi Bridal Suit",
    "Rajasthani Mirror Dress",
    "Bengali Wedding Saree",
    
    # Modern Fusion
    "Indo Western Gown",
    "Party Wear Anarkali",
    "Designer Palazzo Suit",
    "Modern Dhoti Style"  
    
]
   


    


def clean_filename(text: str) -> str:
    """Clean filename to remove invalid characters"""
    return urllib.parse.quote(text, safe='')

def download_image(url: str, save_path: str, headers: dict) -> bool:
    """Download image with proper error handling"""
    try:
        img_response = requests.get(url, headers=headers, stream=True, timeout=30)
        img_response.raise_for_status()
        
        with open(save_path, "wb") as f:
            for chunk in img_response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False

def download_wikimedia_images():
    os.makedirs("indian_dress_images", exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    allowed_formats = ['image/jpeg', 'image/png','image/pdf']
    total_downloads = 0
    
    # Enhanced search terms for better results
    search_variations = [
        "{dress} traditional clothing india",
        "traditional {dress} indian dress",
        "{dress} ethnic wear",
        "{dress} indian fashion",
        "{dress} cultural dress india"
    ]
    
    for dress in dresses:
        print(f"\n{'='*50}")
        print(f"Processing {dress}...")
        images_downloaded = 0
        
        for search_pattern in search_variations:
            if images_downloaded >= 10:  # Limit per dress
                break
                
            search_term = search_pattern.format(dress=dress)
            print(f"\nTrying search term: {search_term}")
            
            params = {
                "action": "query",
                "format": "json",
                "generator": "search",
                "gsrnamespace": 6,
                "gsrsearch": search_term,
                "gsrlimit": 50,  # Increased limit
                "prop": "imageinfo",
                "iiprop": "url|extmetadata|mime"
            }
            
            try:
                print(f"Sending API request for {search_term}...")
                time.sleep(2)  # Increased delay between searches
                
                response = requests.get(
                    "https://commons.wikimedia.org/w/api.php",
                    params=params,
                    headers=headers,
                    timeout=30  # Increased timeout
                )
                response.raise_for_status()
                
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                
                if not pages:
                    print(f"No results found for: {search_term}")
                    continue
                
                print(f"Found {len(pages)} potential images")
                
                for page_id in pages.values():
                    if images_downloaded >= 10:
                        break
                        
                    try:
                        if "imageinfo" not in page_id:
                            continue
                            
                        image_info = page_id["imageinfo"][0]
                        img_url = image_info["url"]
                        mime_type = image_info.get("mime", "")
                        
                        if mime_type not in allowed_formats:
                            print(f"Skipping non-JPG/PNG file: {img_url}")
                            continue
                        
                        file_ext = ".jpg" if mime_type == "image/jpeg" else ".png" 
                        dress_clean = clean_filename(dress)
                        save_path = os.path.join(
                            "indian_dress_images", 
                            f"{dress_clean}_{images_downloaded}{file_ext}"
                        )
                        
                        print(f"\nDownloading {img_url}")
                        if download_image(img_url, save_path, headers):
                            images_downloaded += 1
                            total_downloads += 1
                            print(f"Successfully downloaded ({images_downloaded}/10) for {dress}")
                            time.sleep(1.5)  # Increased delay between downloads
                        
                    except Exception as e:
                        print(f"Error processing image: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Error with search term '{search_term}': {str(e)}")
                continue
            
        print(f"\nCompleted {dress}: {images_downloaded} images downloaded")
    
    print(f"\n{'='*50}")
    print(f"Download process completed! Total images downloaded: {total_downloads}")

if __name__ == "__main__":
    try:
        download_wikimedia_images()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")