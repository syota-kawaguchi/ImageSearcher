import os
import glob

from pathlib import Path

DATA_FOLDER_NAME = "dogs"
RENAME_BASE      = "dog"

project_dir = Path(__file__).resolve().parent.parent
data_dir    = os.path.join(project_dir, 'data', DATA_FOLDER_NAME)
img_paths   = glob.glob(f"{data_dir}/*")

for index, img_path in enumerate(img_paths):
    dirname     = os.path.dirname(img_path)
    ext         = os.path.splitext(img_path)[-1]
    rename_base = RENAME_BASE + str(index) + ext
    os.rename(img_path, os.path.join(dirname, rename_base))