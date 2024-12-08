import os
from PIL import Image

IMAGE_SIZES = {
    "small": 128,
    "middle": 512,
    "big": None,
}


def process_images(source_dir: str, target_dir: str):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                process_image(os.path.join(root, file), source_dir, target_dir)


def process_image(image_path: str, source_dir: str, target_dir: str):
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


def resize_image(image: Image.Image, min_size: int) -> Image.Image:
    ratio = min(image.width, image.height) / min_size
    new_size = (int(image.width / ratio), int(image.height / ratio))
    return image.resize(new_size, Image.Resampling.LANCZOS)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process images into multiple sizes.")
    parser.add_argument("source_dir", help="Directory containing the original images.")
    parser.add_argument("target_dir", help="Directory to store the processed images.")

    args = parser.parse_args()
    process_images(args.source_dir, args.target_dir)
