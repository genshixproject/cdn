from dataclasses import dataclass
import os
import json
import shutil

from PIL import Image


Path = str | os.PathLike[str]
KNOWN_IMAGES_EXT = ["png", "webp"]
KNOWN_OTHER_EXT = ["mp4"]


@dataclass
class Config:
    target_sizes: dict[str, int | None]
    target_extensions: list[str]


def load_config(config_path: Path) -> Config | None:
    if not os.path.exists(config_path):
        return None
    with open(config_path, "r") as file:
        return Config(**json.load(file))


def image_resize(img: Image.Image, resize_to: int | None):
    if resize_to is None:
        return img

    r_coef = (min if resize_to > 0 else max)(img.size) / abs(resize_to)
    return img.resize(map(int, (img.size[0] / r_coef, img.size[1] / r_coef)))


def process_image(source_path: Path, target_dir: Path, config: Config):
    for name, size in config.target_sizes.items():
        img = image_resize(Image.open(source_path), size)

        filename = os.path.splitext(os.path.basename(source_path))[0]
        size_dir = os.path.join(target_dir, filename)
        os.makedirs(size_dir, exist_ok=True)

        for ext in config.target_extensions:
            img.save(os.path.join(size_dir, f"{name}.{ext}"))


def process_file(source_path: Path, target_dir: Path, config: Config):
    filename = os.path.splitext(os.path.basename(source_path))[0]
    size_dir = os.path.join(target_dir, filename)
    os.makedirs(size_dir, exist_ok=True)
    shutil.copy(source_path, target_dir)


def process_dir(current_dir: Path, target_dir: Path, config: Config | None):
    config_current = load_config(os.path.join(current_dir, "config.json")) or config
    if config_current is None:
        raise ValueError("No configuration found.")

    for d in os.listdir(current_dir):
        file = os.path.join(current_dir, d)
        if os.path.isdir(file):
            process_dir(file, os.path.join(target_dir, d), config_current)

        ext = os.path.splitext(file)[1].strip(".")
        if ext in KNOWN_IMAGES_EXT:
            process_image(file, target_dir, config_current)
        elif ext in KNOWN_OTHER_EXT:
            process_file(file, target_dir, config_current)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Process images into multiple sizes and formats."
    )
    parser.add_argument("source_dir", help="Directory containing the original images.")
    parser.add_argument("target_dir", help="Directory to store the processed images.")

    args = parser.parse_args()
    config = load_config(os.path.join(args.source_dir, "config.json"))
    process_dir(args.source_dir, args.target_dir, config)
