import os
import shutil
from PIL import Image
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

class ImageLabeler:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Indian Dress Image Labeler")
        
        # Categories for labeling
        self.categories = [
            "Traditional_Saree", "Modern_Saree",
            "Bridal_Lehenga", "Party_Lehenga",
            "Designer_Anarkali", "Casual_Kurti",
            "Wedding_Dress", "Festival_Wear"
        ]
        
        # Setup UI
        self.setup_ui()
        
        # Image handling
        self.image_files = []
        self.current_image_index = 0
        self.load_images()
        
    def setup_ui(self):
        # Image display
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        
        # Category buttons
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=5)
        
        for category in self.categories:
            btn = ttk.Button(
                self.button_frame, 
                text=category,
                command=lambda c=category: self.label_image(c)
            )
            btn.pack(side=tk.LEFT, padx=5)
            
    def load_images(self):
        input_dir = "indian_dresses"  # Your downloaded images directory
        self.image_files = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.image_files.append(os.path.join(root, file))
        
        if self.image_files:
            self.show_current_image()
            
    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = self.image_files[self.current_image_index]
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            
    def label_image(self, category):
        if self.current_image_index < len(self.image_files):
            # Create category directory if it doesn't exist
            output_dir = os.path.join("labeled_dresses", category)
            os.makedirs(output_dir, exist_ok=True)
            
            # Move and rename the image
            src = self.image_files[self.current_image_index]
            dst = os.path.join(output_dir, f"{category}_{self.current_image_index}.jpg")
            shutil.copy2(src, dst)
            
            # Move to next image
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.show_current_image()
            else:
                self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    labeler = ImageLabeler()
    labeler.run()