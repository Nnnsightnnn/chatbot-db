"""This module gets .pdf file and returns structured data to plug into llm model"""

from unstructured.partition.pdf import partition_pdf
from unstructured.partition.text import partition_text



#structure pdf file
# elements = partition_pdf("static/API_reference.txt", strategy="hi-res")
elements = partition_pdf("static/API_reference.pdf", strategy="hi-res")


"""create new file with elements"""
write_file = open("static/API_reference0.txt", "w")
write_file.write("\n\n".join([str(el) for el in elements]))
