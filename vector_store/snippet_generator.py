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
    snippets = [words[i:i + max_words] for i in range(0, len(words), max_words)]
    return [' '.join(snippet) for snippet in snippets]

def generate_snippets(data, max_words):
    """
    Generate response snippets for each item in the data.
    
    Args:
        data (list): List of items containing responses.
        max_words (int): Maximum number of words in each snippet.
    
    Returns:
        list: Updated data with response snippets.
    """
    for item in data:
        response = item['response']
        snippets = split_response(response, max_words)
        item['response_snippets'] = snippets
    return data

def main():
    """
    Main function to execute the script.
    """
    main_dir = os.path.dirname(os.path.realpath(__file__))
    print(main_dir)
    file_dir = os.path.join(main_dir, "database/memory/")
    print(file_dir)
    json_file_path = os.path.join(file_dir, "memory.json")
    max_words = 15

    data = load_json(json_file_path)

    for item in data:
        response = item['response']
        snippets = split_response(response, max_words)
        for i, snippet in enumerate(snippets):
            output_file_path = os.path.join(file_dir, f"snippet_{i}.json")
            item['response_snippet'] = snippet
            save_json(item, output_file_path)

def merge_data(new_data, existing_data):
    """
    Merge newly generated data with existing data.
    
    Args:
        new_data (list): Newly generated data with response snippets.
        existing_data (list): Existing data loaded from the output file.
    
    Returns:
        list: Merged data.
    """
    id_set = set(item['page_id'] for item in existing_data)
    merged_data = existing_data + [item for item in new_data if item['page_id'] not in id_set]
    return merged_data

if __name__ == '__main__':
    main()
