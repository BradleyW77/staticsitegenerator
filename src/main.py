from copystatic import del_public, copy_dir, get_copied_files

def main():
    del_public()
    copy_dir()
    print(get_copied_files())

main()
