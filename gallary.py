import os
import json
import shutil
from datetime import datetime
from typing import List, Dict

# -----------------------------
# Logger Setup
# -----------------------------
import logging
logging.basicConfig(
    filename="gallery.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("GalleryLogger")

# -----------------------------
# Constants
# -----------------------------
GALLERY_DIR = "gallery_images"
GALLERY_META_FILE = "gallery_metadata.json"

# -----------------------------
# Utility Functions
# -----------------------------
def ensure_directories():
    if not os.path.exists(GALLERY_DIR):
        os.makedirs(GALLERY_DIR)
        logger.info("Created gallery directory.")

def is_valid_image(filename: str) -> bool:
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

def get_file_size(path: str) -> str:
    size_bytes = os.path.getsize(path)
    size_kb = size_bytes / 1024
    return f"{size_kb:.2f} KB"

# -----------------------------
# Gallery Item
# -----------------------------
class GalleryItem:
    def __init__(self, filename: str, title: str, description: str):
        if not is_valid_image(filename):
            raise ValueError("Unsupported file format.")
        self.filename = filename
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "filename": self.filename,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at
        }

    def __str__(self):
        return f"{self.title} - {self.filename} - {self.description}"

# -----------------------------
# Gallery Manager
# -----------------------------
class GalleryManager:
    def __init__(self):
        self.items: List[GalleryItem] = []
        ensure_directories()
        self.load_metadata()

    def add_image(self, source_path: str, title: str, description: str):
        if not os.path.exists(source_path):
            raise FileNotFoundError("Image file not found.")
        filename = os.path.basename(source_path)
        dest_path = os.path.join(GALLERY_DIR, filename)

        shutil.copy2(source_path, dest_path)
        item = GalleryItem(filename, title, description)
        self.items.append(item)
        logger.info("Added image: %s", filename)
        self.save_metadata()

    def delete_image(self, title: str):
        item = next((x for x in self.items if x.title == title), None)
        if item:
            self.items.remove(item)
            try:
                os.remove(os.path.join(GALLERY_DIR, item.filename))
            except FileNotFoundError:
                pass
            logger.info("Deleted image: %s", title)
            self.save_metadata()
            return True
        logger.warning("Image not found: %s", title)
        return False

    def list_images(self) -> List[Dict]:
        return [item.to_dict() for item in self.items]

    def display_gallery(self):
        print("\n=== Image Gallery ===")
        if not self.items:
            print("No images available.")
            return
        for item in self.items:
            size = get_file_size(os.path.join(GALLERY_DIR, item.filename))
            print(f"{item.title} | {item.filename} | {item.description} | {size}")

    def save_metadata(self):
        with open(GALLERY_META_FILE, 'w') as f:
            json.dump([item.to_dict() for item in self.items], f, indent=2)
        logger.info("Saved metadata to %s", GALLERY_META_FILE)

    def load_metadata(self):
        try:
            with open(GALLERY_META_FILE, 'r') as f:
                data = json.load(f)
                self.items = [
                    GalleryItem(d["filename"], d["title"], d["description"])
                    for d in data
                ]
            logger.info("Loaded metadata from file.")
        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning("No existing metadata file found.")

# -----------------------------
# Menu
# -----------------------------
def print_menu():
    print("\n=== Gallery Menu ===")
    print("1. Add Image")
    print("2. Delete Image")
    print("3. List Images")
    print("4. Save Metadata")
    print("5. Load Metadata")
    print("0. Exit")

# -----------------------------
# Main Execution
# -----------------------------
def main():
    gallery = GalleryManager()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                source = input("Enter path to image: ").strip()
                title = input("Enter image title: ").strip()
                description = input("Enter image description: ").strip()
                gallery.add_image(source, title, description)
                print("Image added.")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            title = input("Enter title of image to delete: ").strip()
            success = gallery.delete_image(title)
            print("Image deleted." if success else "Image not found.")

        elif choice == "3":
            gallery.display_gallery()

        elif choice == "4":
            gallery.save_metadata()
            print("Metadata saved.")

        elif choice == "5":
            gallery.load_metadata()
            print("Metadata loaded.")

        elif choice == "0":
            print("Exiting Gallery Manager.")
            break

        else:
            print("Invalid option. Please try again.")

# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()

