import os
from io import StringIO
from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean_non_ascii_chars

# Define the input directory and output directory paths
input_directory_path = "input/"
output_directory_path = "output/"

# Get the list of files in the input directory
file_list = os.listdir(input_directory_path)

# Process each file in the input directory
for file_name in file_list:
    # Check if the file is a PDF
    if file_name.endswith(".pdf"):
        input_file_path = os.path.join(input_directory_path, file_name)
        output_file_path = os.path.join(output_directory_path, f"{file_name[:-4]}_cleaned.txt")

        # Structure PDF file
        elements = partition_pdf(input_file_path)

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

        print(f"Non-ASCII characters have been successfully removed from {file_name} and the cleaned content saved to {output_file_path}")
