# Indian Traditional Dress Image Dataset

> A comprehensive image collection and labeling system for Indian traditional dress research using Python.

## 📁 Project Structure
```plaintext
research/
├── dresses1.py           # Image crawler script
├── label_images.py       # Image labeling system
├── indian_dresses/       # Downloaded images
├── labeled_dresses/      # Labeled dataset
└── dataset_metadata.json # Research metadata
```

## 🚀 Features
- Automated image collection from Google Images
- Hierarchical classification system
- Research-grade metadata tracking
- Expert-validated categorization
- Cross-platform compatibility

## 📋 Categories
- **Traditional**: Classical Saree, Regional Saree
- **Contemporary**: Modern Saree, Indo-Western
- **Bridal**: Wedding Lehenga, Bridal Saree
- **Ethnic**: Anarkali, Salwar Kameez
- **Festival**: Festive Wear, Ceremonial Dress

## 🛠️ Setup

### Prerequisites
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Install Dependencies
```bash
pip install icrawler Pillow
```

## 📥 Image Collection
```bash
python dresses1.py
```
This will:
- Create category-specific folders
- Download 800 images across categories
- Organize files automatically

## 🏷️ Image Labeling
```bash
python label_images.py
```
Features:
- Visual labeling interface
- Metadata tracking
- Research documentation
- Hierarchical classification

## 📊 Dataset Statistics
- Total Images: 800
- Categories: 20
- Format: JPG/PNG
- Resolution: Various

## 📝 Research Usage
The dataset and labeling system are designed for:
- Computer Vision Research
- Fashion Classification
- Cultural Pattern Recognition
- Machine Learning Applications

## 📚 Citation
```bibtex
@dataset{indian_dress_dataset,
  title={Indian Traditional Dress Image Dataset},
  year={2024},
  author={Your Name},
  institution={Your Institution}
}
```

## 🔍 Metadata
Generated `dataset_metadata.json` includes:
- Image properties
- Classification timestamps
- Category hierarchies
- Dataset statistics

## 📄 License
MIT License

## 🤝 Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Submit pull request

## 📧 Contact
Your Name - your.email@domain.com

---
*This project is part of research work on Indian traditional dress classification.*
