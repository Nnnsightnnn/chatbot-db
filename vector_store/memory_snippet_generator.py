import json
import os

def load_json(file_path):
    # Load JSON data from a file
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_json(data, file_path):
    # Save JSON data to a file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def split_response(response, max_words):
    # Split a response into smaller snippets based on the maximum number of words
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
    # Generate response snippets for each item in the data
    updated_data = []

    for item in data:
        page_id = item.get('page id', None)
        response = item['response']
        snippets = split_response(response, max_words)
        response_snippets = []

        for i, snippet in enumerate(snippets):
            snippet_data = {'page id': page_id, 'snippet': snippet}
            response_snippets.append(snippet_data)
            main_dir = os.path.dirname(os.path.realpath(__file__))
            file_dir = os.path.join(main_dir, "database/memory/")
            output_file_path = os.path.join(file_dir, f"snippet_{page_id}_{i}.json")
            save_json(snippet_data, output_file_path)

        item['response_snippets'] = response_snippets
        updated_data.append(item)

    return updated_data

def main(max_words=15):
    main_dir = os.path.dirname(os.path.realpath(__file__))
    file_dir = os.path.join(main_dir, "database/memory/")
    json_file_path = os.path.join(file_dir, "memory.json")

    data = load_json(json_file_path)
    generate_snippets(data, max_words)

if __name__ == '__main__':
    main()
