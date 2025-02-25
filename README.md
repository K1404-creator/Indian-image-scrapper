# Wikimedia Indian Culture Image Scraper

> Python tool for downloading Indian dress and cuisine images using Wikimedia Commons API.

## 🎯 Features
- Multi-category image scraping (Dresses & Cuisine)
- Smart search patterns and rate limiting
- Progress tracking and error handling
  

## 📂 Project Structure
```bash
wikimedia-scraper/
├── src/
│   ├── scraper.py    # Base scraper class
│   ├── dresses.py    # Traditional dress scraper
│   └── dishes.py     # Indian cuisine scraper
```

## 🔧 Setup & Usage
```bash
# Install
pip install requests
pip install beautifulsoup4

# Run scrapers
python src/dresses.py  # For dresses
python src/dishes.py   # For cuisine
```

## 📑 Categories

### 👗 Dresses
- Traditional: Saree, Lehenga, Kurta
- Wedding: Bridal wear, Groom's attire
- Regional: South Indian, Punjabi, Rajasthani
- Festival: Diwali, Garba, Eid
- Modern: Indo-western, Designer wear

### 🍱 Cuisine
- Street Food: Chaat, Samosa, Vada Pav
- Main Course: Butter Chicken, Biryani
- South Indian: Dosa, Idli, Uttapam
- Breads: Naan, Roti, Paratha
- Desserts: Gulab Jamun, Rasgulla


## 📄 License
MIT License

---
Made for Indian cultural preservation | © 2025
