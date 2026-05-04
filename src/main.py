from copystatic import del_public, copy_dir, get_copied_files
from generate_page import generate_pages_recursive

def main():
    del_public()
    copy_dir()
    print(get_copied_files())
    generate_pages_recursive("content", "template.html", "public")

main()
