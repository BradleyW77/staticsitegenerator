import os

from markdown_blocks import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    page_title = extract_title(markdown)
    page = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        print(f"Writing page to {dest_path}")
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
            generate_page(item_path, template_path, dest_path, basepath)
        elif os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(item_path, template_path, new_dest_dir, basepath)
