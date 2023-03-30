"""This module gets .pdf file and returns structured data to plug into llm model"""

from unstructured.partition.pdf import partition_pdf

#structure pdf file
elements = partition_pdf("static/7230.pdf", strategy="hi_res")

"""create new file with elements"""
write_file = open("static/elements.pdf", "w")
write_file.write("\n\n".join([str(el) for el in elements]))
