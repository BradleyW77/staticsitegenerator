import sys

from copystatic import del_dir, copy_dir, get_copied_files
from generate_page import generate_pages_recursive

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    del_dir()
    copy_dir()
    print(get_copied_files())
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
