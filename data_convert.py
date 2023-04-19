"""This module gets .pdf file and returns structured data to plug into llm model"""

from unstructured.partition.pdf import partition_pdf
from unstructured.partition.text import partition_text
from unstructured.cleaners.core import clean_non_ascii_chars


#structure pdf file
# elements = partition_pdf("static/elder_evils", strategy="hi-res")
# elements = partition_pdf("static/elder_evils.pdf", strategy="hi-res")
elements = partition_text("static/elder_evils.txt", encoding="utf-8")

elements = clean_non_ascii_chars(str(elements))

"""create new file with elements"""
write_file = open("static/elder_evils.txt", "w", encoding="utf-8")
write_file.write("\n\n".join([str(el) for el in elements]))
