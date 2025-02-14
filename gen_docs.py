import os
import subprocess
import ast
import sys


def install_pdoc():
    """Install pdoc if it's not already installed."""
    try:
        import pdoc
    except ImportError:
        print("pdoc is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pdoc"])
        print("pdoc installed successfully.")


def get_package_name_from_setup():
    """Read package name from setup.py file."""
    setup_file = "setup.py"

    # Open and parse setup.py to get the package name
    with open(setup_file, "r") as f:
        setup_code = f.read()

    # Parse the setup.py code using AST to safely extract the package name
    tree = ast.parse(setup_code)
    for node in ast.walk(tree):
        # Check if the node is a call to the setup function
        if isinstance(node, ast.Call):
            # Check if the function is 'setup', it could be accessed as 'setuptools.setup'
            if isinstance(node.func, ast.Name) and node.func.id == "setup":
                for keyword in node.keywords:
                    if keyword.arg == "name":
                        return keyword.value.value  # type: ignore # Use 'value' instead of 's'
            elif isinstance(node.func, ast.Attribute) and node.func.attr == "setup" and isinstance(node.func.value, ast.Name) and node.func.value.id == "setuptools":
                # If it's accessed through 'setuptools.setup', get the package name
                for keyword in node.keywords:
                    if keyword.arg == "name":
                        return keyword.value.value  # type: ignore # Use 'value' instead of 's'

    return None  # In case the package name is not found


def generate_docs(package_name):
    """Generate documentation for the package using pdoc."""
    if not package_name:
        raise ValueError("Package name could not be extracted from setup.py")

    # Generate docs using pdoc
    subprocess.run(["pdoc", "--output-dir", "docs", package_name], check=True)
    print(
        f"Documentation for '{package_name}' generated successfully in the 'docs/' folder.")


if __name__ == "__main__":
    # Ensure pdoc is installed
    install_pdoc()

    # Get the package name from setup.py
    package_name = get_package_name_from_setup()

    # Generate the documentation
    try:
        generate_docs(package_name)
    except Exception as e:
        print(f"Error generating documentation: {e}")
