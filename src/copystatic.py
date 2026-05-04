import os
import shutil

def del_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")

copied_files = []

def copy_dir(file_path="./static", dst_path="./public"):
    if os.path.exists(file_path):
        static_contents = os.listdir(file_path)
        for item in static_contents:
            item_static_path = os.path.join(file_path, item)
            item_public_path = os.path.join(dst_path, item)
            if os.path.isfile(item_static_path):
                shutil.copy(item_static_path, item_public_path)
                copied_files.append(item_public_path)
            else:
                os.mkdir(item_public_path)
                copy_dir(item_static_path, item_public_path)

def get_copied_files():
    return copied_files
