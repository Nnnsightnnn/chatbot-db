import json
import os

def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_json(data, file_path):
    """
    Save JSON data to a file.

    Args:
        data (dict): JSON data to be saved.
        file_path (str): Path to save the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def split_response(response, max_words):
    """
    Split a response into smaller snippets based on the maximum number of words.

    Args:
        response (str): The response to be split.
        max_words (int): Maximum number of words in each snippet.

    Returns:
        list: List of response snippets.
    """
    words = response.split()
    snippets = []
    current_snippet = []
    word_count = 0

    for word in words:
        if word_count + 1 <= max_words:
            current_snippet.append(word)
            word_count += 1
        else:
            snippets.append(' '.join(current_snippet))
            current_snippet = [word]
            word_count = 1

    if current_snippet:
        snippets.append(' '.join(current_snippet))

    return snippets

def generate_snippets(data, max_words):
    """
    Generate response snippets for each item in the data.

    Args:
        data (list): List of items containing responses.
        max_words (int): Maximum number of words in each snippet.

    Returns:
        list: List of response snippets.
    """
    snippets = []

    for item in data:
        response = item['response']
        item_snippets = split_response(response, max_words)
        snippets.extend(item_snippets)

    return snippets

def main():
    """
    Main function to execute the script.
    """
    main_dir = os.path.dirname(os.path.realpath(__file__))
    file_dir = os.path.join(main_dir, "database/memory/")
    json_file_path = os.path.join(file_dir, "memory.json")
    max_words = 30

    data = load_json(json_file_path)
    snippets = generate_snippets(data, max_words)

    for i, snippet in enumerate(snippets):
        output_file_path = os.path.join(file_dir, f"snippet_{i}.json")
        snippet_data = {'response_snippet': snippet}
        save_json(snippet_data, output_file_path)

if __name__ == '__main__':
    main()
