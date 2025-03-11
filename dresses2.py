from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import hashlib
from PIL import Image
from io import BytesIO

class MultiSourceScraper:
    def __init__(self):
        self.base_dir = f"indian_dresses_dataset_{time.strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.base_dir, exist_ok=True)
        self.setup_logging()
        self.setup_webdriver()
        self.download_count = 0

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{self.base_dir}/scraping.log'),
                logging.StreamHandler()  # Add console output
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def is_valid_image(self, content):
        try:
            img = Image.open(BytesIO(content))
            return img.size[0] >= 400 and img.size[1] >= 400
        except:
            return False

    def _scrape_google(self, category: str, save_dir: str):
        self.logger.info(f"Starting Google scraping for {category}")
        crawler = GoogleImageCrawler(
            storage={'root_dir': save_dir},
            feeder_threads=1,
            parser_threads=1,
            downloader_threads=4
        )
        
        filters = dict(
            size='large',
            type='photo',
            license='commercial,modify'
        )
        
        try:
            crawler.crawl(
                keyword=f"Indian {category} dress traditional professional",
                max_num=200,  # Increased number
                min_size=(400, 400),
                filters=filters
            )
            self.logger.info(f"Completed Google scraping for {category}")
        except Exception as e:
            self.logger.error(f"Google error for {category}: {str(e)}")

    def _scrape_ecommerce(self, category: str, save_dir: str):
        self.logger.info(f"Starting E-commerce scraping for {category}")
        sites = {
            "utsavfashion.com": "/search/?q=",
            "cbazaar.com": "/search/",
            "mirraw.com": "/search?q=",
            "fashion.mirraw.com": "/search?q="
        }
        
        for site, search_path in sites.items():
            try:
                url = f"https://www.{site}{search_path}{category.replace(' ', '+')}"
                self.logger.info(f"Scraping {url}")
                self.driver.get(url)
                time.sleep(5)  # Wait for page load
                
                images = self.driver.find_elements(By.TAG_NAME, "img")
                self.logger.info(f"Found {len(images)} images on {site}")
                
                for idx, img in enumerate(images[:100]):  # Increased from 50
                    try:
                        src = img.get_attribute('src')
                        if src and src.startswith('http'):
                            response = requests.get(src, timeout=10)
                            if response.status_code == 200 and self.is_valid_image(response.content):
                                img_hash = hashlib.md5(response.content).hexdigest()
                                img_path = os.path.join(save_dir, f"{category}_{site}_{idx}_{img_hash}.jpg")
                                with open(img_path, 'wb') as f:
                                    f.write(response.content)
                                self.download_count += 1
                                if self.download_count % 10 == 0:
                                    self.logger.info(f"Downloaded {self.download_count} images")
                    except Exception as e:
                        self.logger.error(f"Error downloading image: {str(e)}")
                        continue
                
            except Exception as e:
                self.logger.error(f"Error scraping {site}: {str(e)}")
                continue

    def scrape_category(self, category: str):
        category_dir = os.path.join(self.base_dir, category.replace(" ", "_"))
        os.makedirs(category_dir, exist_ok=True)
        
        self.logger.info(f"Starting scraping for category: {category}")
        self._scrape_google(category, category_dir)
        self._scrape_ecommerce(category, category_dir)
        
        count = len(os.listdir(category_dir))
        self.logger.info(f"Completed {category}: {count} images downloaded")
        return count

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

# Usage
if __name__ == "__main__":
    dress_categories = [
        "Saree", "Lehenga", "Salwar Kameez", "Anarkali", "Kurti",
        "Designer Saree", "Bridal Lehenga", "Traditional Saree"
    ]
    
    scraper = MultiSourceScraper()
    
    for category in dress_categories:
        count = scraper.scrape_category(category)
        print(f"Downloaded {count} images for {category}")