"""This module gets .pdf file and returns structured data to plug into llm model"""

import os
from unstructured.partition.pdf import partition_pdf


elements = partition_pdf("static/slatebook2.pdf")

print("\n\n".join([str(el) for el in elements]))