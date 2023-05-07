import os
import glob
from pathlib import Path

from PIL import Image

DATA_FOLDER_NAME = "dogs"
RESIZE_WIDTH     = 512
RESIZE_HEIGHT    = 512

def main():
    project_dir = Path(__file__).resolve().parent.parent
    data_dir    = os.path.join(project_dir, 'data', DATA_FOLDER_NAME)
    save_dir    = os.path.join(project_dir, 'data','resized', DATA_FOLDER_NAME)
    os.makedirs(save_dir, exist_ok=True)

    img_paths   = glob.glob(f"{data_dir}/*")
    for img_path in img_paths:
        base_name   = os.path.basename(img_path)
        img         = Image.open(img_path)
        # 正方形に整形
        img_square  = crop_max_square(img)
        resized_img = img_square.resize((RESIZE_WIDTH, RESIZE_HEIGHT))
        resized_img.save(os.path.join(save_dir, base_name))

def crop_center(img:Image, crop_width, crop_height):
    img_width, img_height = img.size
    return img.crop(((img_width  - crop_width)  // 2,
                     (img_height - crop_height) // 2,
                     (img_width  + crop_width)  // 2,
                     (img_height + crop_height) // 2))

def crop_max_square(img:Image):
    return crop_center(img, min(img.size), min(img.size))

if __name__ == "__main__":
    main()