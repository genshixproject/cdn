import os
from PIL import Image

IMAGE_SIZES = {
    "small": 128,
    "middle": 512,
    "big": None,
}

TARGET_EXTENSION = "webp"


def process_images(source_dir, target_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                process_image(os.path.join(root, file), source_dir, target_dir)


def process_image(image_path, source_dir, target_dir):
    image = Image.open(image_path).convert("RGB")
    base_path = os.path.relpath(image_path, source_dir)
    base_name, _ = os.path.splitext(base_path)

    for size_name, min_size in IMAGE_SIZES.items():
        target_path = os.path.join(
            target_dir, base_name, f"{size_name}.{TARGET_EXTENSION}"
        )
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        if min_size is None:
            image.save(target_path, format=TARGET_EXTENSION.upper())
        else:
            resized_image = resize_image(image, min_size)
            resized_image.save(target_path, format=TARGET_EXTENSION.upper())


def resize_image(image, min_size):
    ratio = min(image.width, image.height) / min_size
    new_size = (int(image.width / ratio), int(image.height / ratio))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def copy_cname(target_dir):
    with open("CNAME") as f:
        domain = f.read().strip()

    with open(os.path.join(target_dir, "CNAME"), "w") as f:
        f.write(domain)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process images into multiple sizes and formats."
    )
    parser.add_argument("source_dir", help="Directory containing the original images.")
    parser.add_argument("target_dir", help="Directory to store the processed images.")

    args = parser.parse_args()

    copy_cname(args.target_dir)
    process_images(args.source_dir, args.target_dir)
