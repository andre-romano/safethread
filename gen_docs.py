import os
import subprocess
import ast
import sys
import shutil


def install_pdoc():
    """Install pdoc if it's not already installed."""
    try:
        import pdoc
    except ImportError:
        print("pdoc is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdoc"])
        print("pdoc installed successfully.")


def install_html2text():
    """Install html2text if it's not already installed."""
    try:
        import html2text
    except ImportError:
        print("html2text is not installed. Installing now...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "html2text"])
        print("html2text installed successfully.")


def get_package_name_from_setup():
    """Read package name from setup.py file."""
    setup_file = "setup.py"

    with open(setup_file, "r") as f:
        setup_code = f.read()

    tree = ast.parse(setup_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "setup":
                for keyword in node.keywords:
                    if keyword.arg == "name":
                        return keyword.value.value  # type: ignore
            elif isinstance(node.func, ast.Attribute) and node.func.attr == "setup" and isinstance(node.func.value, ast.Name) and node.func.value.id == "setuptools":
                for keyword in node.keywords:
                    if keyword.arg == "name":
                        return keyword.value.value  # type: ignore
    return None


def clean_docs():
    """Delete all contents of the docs/ folder recursively."""
    docs_dir = "docs"
    if os.path.exists(docs_dir):
        print("Cleaning existing documentation files in 'docs/'...")
        shutil.rmtree(docs_dir)
        print("Existing documentation deleted.")
    else:
        print("No existing documentation found. Creating 'docs/' folder.")
    os.makedirs(docs_dir)


def generate_docs(package_name):
    """Generate documentation for the package using pdoc (output: HTML files)."""
    if not package_name:
        raise ValueError("Package name could not be extracted from setup.py")

    clean_docs()  # Clean the docs folder before generating new docs

    subprocess.run(["pdoc", "--output-dir", "docs", package_name], check=True)
    print(
        f"Documentation for '{package_name}' generated successfully in the 'docs/' folder.")


def generate_markdown():
    """Convert all HTML files in the docs/ folder to Markdown format."""
    import html2text

    docs_dir = "docs"
    for root, _, files in os.walk(docs_dir):
        for file_name in files:
            if file_name.endswith(".html"):
                html_path = os.path.join(root, file_name)
                md_path = os.path.splitext(html_path)[0] + ".md"

                with open(html_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()

                md_content = html2text.html2text(html_content)

                with open(md_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(md_content)

                print(f"Converted {html_path} to {md_path}")


if __name__ == "__main__":
    install_pdoc()
    install_html2text()
    package_name = get_package_name_from_setup()
    try:
        generate_docs(package_name)
        generate_markdown()
    except Exception as e:
        print(f"Error generating documentation: {e}")
