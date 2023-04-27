"""This module converts PDF files to text files 
and removes non-ASCII characters from the text files."""
import os
from io import StringIO
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean_non_ascii_chars

# Define the input directory and output directory paths
INPUT_DIRECTORY_PATH = "pdf_input/"
OUTPUT_DIRECTORY_PATH = "txt_output/"

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
print(parent_dir)

# Ensure the input directory exists
directory_path = os.path.join(parent_dir, f"chatbot-db/{INPUT_DIRECTORY_PATH}")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(directory_path)
# Ensure the output directory exists
directory_path = os.path.join(parent_dir, f"chatbot-db/{OUTPUT_DIRECTORY_PATH}")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Get the list of files in the input directory
file_list = os.listdir(INPUT_DIRECTORY_PATH)

# Process each file in the input directory
for file_name in file_list:
    # Check if the file is a PDF
    if file_name.endswith(".pdf"):
        input_DIRECTORY_PATHfile_path = os.path.join(INPUT_DIRECTORY_PATH, file_name)
        output_file_path = os.path.join(OUTPUT_DIRECTORY_PATH, f"{file_name[:-4]}_cleaned.txt")

        # Structure PDF file
        elements = partition_pdf(input_DIRECTORY_PATHfile_path)

        # Write the elements into a StringIO object
        elements_str = StringIO()
        elements_str.write("\n\n".join([str(el) for el in elements]))

        # Read the contents of the StringIO object
        elements_str.seek(0)
        file_content = elements_str.read()

        # Apply the clean_non_ascii_chars function on the file content
        cleaned_content = clean_non_ascii_chars(file_content)

        # Write the cleaned content to the output file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(cleaned_content)

        print(f"Non-ASCII characters have been successfully"
               f"removed from {file_name} and the cleaned content saved to {output_file_path}")

# Path: data_convert.py
