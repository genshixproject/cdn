import os
from PIL import Image

# Global settings for image sizes
IMAGE_SIZES = {
    "small": 128,  # Minimum dimension for "small"
    "middle": 512,  # Minimum dimension for "middle"
    "big": None,  # Original size (no resizing)
}

def process_images(source_dir, target_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                process_image(os.path.join(root, file), source_dir, target_dir)

def process_image(image_path, source_dir, target_dir):
    image = Image.open(image_path)
    base_path = os.path.relpath(image_path, source_dir)
    base_name, _ = os.path.splitext(base_path)
    
    for size_name, min_size in IMAGE_SIZES.items():
        target_path = os.path.join(target_dir, base_name, f"{size_name}.png")
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        if min_size is None:  # "big" size: keep original dimensions
            image.save(target_path)
        else:
            resize_image(image, min_size).save(target_path)

def resize_image(image, min_size):
    ratio = min(image.width, image.height) / min_size
    new_size = (int(image.width / ratio), int(image.height / ratio))
    return image.resize(new_size, Image.ANTIALIAS)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process images into multiple sizes.")
    parser.add_argument("source_dir", help="Directory containing the original images.")
    parser.add_argument("target_dir", help="Directory to store the processed images.")

    args = parser.parse_args()
    process_images(args.source_dir, args.target_dir)
