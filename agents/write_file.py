"""this module write input to file"""
import os
from dotenv import load_dotenv

load_dotenv()

def write_input_to_py_file(input_text: str, file_name: str, directory: str = "ChatbotDB\code"):
    """Write the input text to a .py file in the specified directory."""
    # Get the absolute path of the parent directory
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

    # Ensure the directory exists
    directory_path = os.path.join(parent_dir, directory)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Sanitize the file name and add .py extension if not present
    if not file_name.endswith(".py"):
        file_name = f"{file_name}.py"

    # Write the input text to the .py file in the specified directory
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(input_text)


"""
if __name__ == "__main__":
    user_input = input("Enter your Python code: ")
    file_name = input("Enter the desired file name (without .py extension): ")
    write_input_to_py_file(user_input, file_name)
    print(f"Your code has been saved to /code/{file_name}.py")
"""
