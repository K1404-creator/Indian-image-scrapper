from icrawler.builtin import GoogleImageCrawler
import os

# Define your dress categories (ensure you have around 20-25 strings)
dress_categories = [
    "Saree", "Lehenga", "Salwar Kameez", "Anarkali", "Kurti",
    "Choli", "Ghagra", "Designer Saree", "Banarasi Saree", 
    "Kanjeevaram Saree", "Bandhani Saree", "Embroidered Lehenga", 
    "Mirror Work Dress", "Bridal Saree", "Modern Saree", "Vintage Saree",
    "Ethnic Indian Dress", "Traditional Indian Dress", "Festive Indian Dress", "Contemporary Saree"
]

# Calculate the number of images per category (assuming you have 20 categories)
images_per_category = 800 // len(dress_categories)

# Base directory to store images
base_dir = "indian_dresses"
os.makedirs(base_dir, exist_ok=True)

for category in dress_categories:
    # Create a subdirectory for each dress type
    category_folder = os.path.join(base_dir, category.replace(" ", "_"))
    os.makedirs(category_folder, exist_ok=True)
    
    # Define the search query
    query = f"Indian {category} dress"
    
    print(f"Downloading {images_per_category} images for '{query}'...")
    
    # Initialize the crawler with the storage set to the category folder
    crawler = GoogleImageCrawler(storage={'root_dir': category_folder})
    
    # Crawl images for the query. Adjust filters if necessary.
    crawler.crawl(keyword=query, max_num=images_per_category)
    
print("Download completed!")
