"""this module splits a given text into chuncks of a given size"""
from transformers import GPT2TokenizerFast
from langchain.text_splitter import CharacterTextSplitter
from langchain.agents import create_openapi_agent

#from langchain.text_splitter import TokenTextSplitter

#instance of a tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')

# this is a long document that we split up
with open('static/slatebook.txt', "r", encoding="utf-8") as f:
    slatebook = f.read()

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(slatebook)

# print 1st chunk
print(texts[5])

#create new file with elements
write_file = open("static/split.txt", "w", encoding="utf-8")
write_file.write("\n\n".join([str(el) for el in texts]))
write_file.close()

# Path: text_split.py
