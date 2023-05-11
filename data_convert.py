import os
from io import StringIO
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean_non_ascii_chars

# Define the input directory and output directory paths
INPUT_DIRECTORY_PATH = "pdf_input/"
MEMORY_DIRECTORY_PATH = "vector_store/database/memory/"
OUTPUT_DIRECTORY_PATH = "txt_output/"

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

# Ensure the input directory exists
directory_path = os.path.join(parent_dir, f"chatbot-db/{INPUT_DIRECTORY_PATH}")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Ensure the output directory exists
directory_path = os.path.join(parent_dir, f"chatbot-db/{OUTPUT_DIRECTORY_PATH}")
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Get the list of files in the input directory
file_list = os.listdir(INPUT_DIRECTORY_PATH)

# Process each file in the input directory
for file_name in file_list:
    file_content = ""
    if file_name.endswith(".pdf"):
        input_file_path = os.path.join(INPUT_DIRECTORY_PATH, file_name)
        output_file_path = os.path.join(OUTPUT_DIRECTORY_PATH, f"{file_name[:-4]}_cleaned.txt")

        # Structure PDF file
        elements = partition_pdf(input_file_path)

        # Write the elements into a StringIO object
        elements_str = StringIO()
        elements_str.write("\n\n".join([str(el) for el in elements]))

        # Read the contents of the StringIO object
        elements_str.seek(0)
        file_content = elements_str.read()

    elif file_name.endswith(".json"):
        input_file_path = os.path.join(INPUT_DIRECTORY_PATH, file_name)
        output_file_path = os.path.join(OUTPUT_DIRECTORY_PATH, f"{file_name[:-5]}_cleaned.txt")

        # Load JSON content
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            json_content = input_file.read()

        # Convert JSON content to a string representation
        file_content = json_content

    elif file_name.endswith(".txt"):
        input_file_path = os.path.join(INPUT_DIRECTORY_PATH, file_name)
        output_file_path = os.path.join(OUTPUT_DIRECTORY_PATH, f"{file_name[:-4]}_cleaned.txt")

        # Read the contents of the text file
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            file_content = input_file.read()

    if file_content:
        # Apply the clean_non_ascii_chars function on the file content
        cleaned_content = clean_non_ascii_chars(file_content)

        # Write the cleaned content to the output file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(cleaned_content)

        print(f"Non-ASCII characters have been successfully"
               f" removed from {file_name} and the cleaned content saved to {output_file_path}")

"""This code checks if a file in the input directory is a JSON file and loads its content using the `json` module. 
The JSON content is then converted to a string representation using `json.dumps()`. The rest of the code remains the same, 
as it cleans the non-ASCII characters and writes the cleaned content to the output file."""

# Path: data_convert.py