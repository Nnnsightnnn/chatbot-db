"""this module is used to generate a novel based on a seed text."""

import os
import json
import textwrap
import openai

from dotenv import load_dotenv
from langchain.chat_models.openai import ChatOpenAI
from agents.doc_search import local_doc_search
import config

load_dotenv()

def generate_novel():
    """This function generates a novel based on a seed text."""
    # Initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                     max_tokens=config.OPENAI_MAX_TOKENS,
                     api_key=config.OPENAI_API_KEY, streaming=True)
    uri = local_doc_search(query="moutain dwarf monk", k=2)
    naristrune = local_doc_search(query="deep dragon", k=2)
    seed_text = f"""
        Two winding tales. The first tale is about, Uri, a mountain dwarf monk, seeking lost dwarven artifacts, {uri}
        exploring the Underdark; The second tale is about Naristrune, an evil deep dragon, {naristrune}.     
    """
    prompt_text = f"""
     Step 1
        Create an extensive outline for a novel based on this {seed_text}.
        Follow this outline template, but feel free to add more details if you wish:
        The novel is set in (insert) setting.
        The main character is (insert) main character.
        The main character's goal is to (insert) goal.
        The main character's obstacles are (insert) obstacles.
        The main character's enemies are (insert) enemies.
        The novel ends with (insert) ending.
    
    Step 2
        Build a ladder of events from the outline to reach the ending in prose . 
    Step 2 
        Use the ladder to create a detailed plot for this novel in prose.
        De-limit the plot with a '|' to idicate when new part should start to the novel.
    Step 3
        Modifiy the detailed plot to include scenes and de-limit with a '|'.
    """

    # File Storage location
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print(dir_path)
    folder_path = os.path.join(dir_path, 'novel')
    print(folder_path)
    file_path = os.path.join(folder_path, 'broad_plot.json')
    print(file_path)

    print("Generating a novel based on the seed text...")
    # Step 1: Generate a broad plot
    broad_plot = llm.call_as_llm(prompt_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(broad_plot, file)
    print("The broad plot has been successfully written to 'broad_plot.json")

    # Step 2: Iterate through plot in parts, giving it more depth
    with open(file_path, 'r', encoding='utf-8') as file:
        second_plot = json.load(file)
    detailed_plot = []
    part_id = 0
    for chunk in second_plot:
    # Get only the text from the JSON and split it
        chunk = chunk.split("|")
        for point in chunk:
            print(f"Generating a detailed plot for part {part_id}")
            parts = llm.call_as_llm(f"""
            You are R.A. Salvatore, the fantasy writer, 
            converting a plot about Uri, a dwarven monk and
            Naristrune, a deep dragon into a series of chapters.
            Create a more detailed and descriptive version in prose of:
            {point}, de-limit where new chapters should start with '|'
            """)
            detailed_plot.append({"part_id": part_id, "text": parts})
            part_id += 1
    detail_file_path = os.path.join(folder_path, 'detailed_plot.json')

    with open(detail_file_path, 'w', encoding='utf-8') as file:
        json.dump(detailed_plot, file)
    print("The detailed plot has been successfully written to 'detailed_plot.json")

    # Step 3: Iterate through detailed plot, creating descriptive scenes
    with open(detail_file_path, 'r', encoding='utf-8') as file:
        plot_chapter = json.load(file)
    scene_descriptions = []
    chapter_id = 0
    for parts in plot_chapter:
        print(f"Generating a descriptive scenes for chapter {chapter_id}")
    # Get only the text from the JSON and split it
        plot_parts = plot_parts.split("|")
        for plot_part in plot_parts:
            scene_prompt = f"""
            You are R.A. Salvatore, you're writing about Uri, a dwarven monk and
            Naristrune, a deep dragon generate highly atmospheric and detailed scenes in prose from: {plot_part}, 
            and de-limit with a '|', from this section of a plot:
            """
            scene = llm.call_as_llm(scene_prompt)
            scene_descriptions.append(
                    {"chapter_id": chapter_id, "text": scene,})
            chapter_id += 1
    scene_file_path = os.path.join(folder_path, 'scene_descriptions.json')
    with open(scene_file_path, 'w', encoding='utf-8') as file:
        json.dump(scene_descriptions, file)
    print("The scene descriptions have been successfully written to 'scene_descriptions.json'")

    # Step 4: Iterate through each scene, creating final, beautifully descriptive scenes
    with open(scene_file_path, 'r', encoding='utf-8') as file:
        scene_descriptions = json.load(file)
    final_novel = []
    page_id = 0
    for chapter in scene_descriptions:
        print(f"Generating a scene descriptions for page {page_id}")
        scenes = scenes.split("|")
        for scene in scenes:
            final_edit_prompt = f"""
            You are R.A. Salvatore, you're writing about Uri, a dwarven monk and
        Naristrune, a deep dragon
            convert each of these scenes into several highly atmospheric and conversation laden in prose scenes:
            {scene}
            """
            final_edit = llm.call_as_llm(final_edit_prompt)
            final_novel.append(
                {"page_id": page_id, "text": final_edit, "chapter_id": chapter["chapter_id"]})
            page_id += 1
    final_file_path = os.path.join(folder_path, 'final_novel.json')
    with open(final_file_path, 'w', encoding='utf-8') as file:
        json.dump(final_novel, file)
    print("The final novel has been successfully written to 'final_novel.json'")

    # Write final novel to a text file
    with open(final_file_path, 'r', encoding='utf-8') as file:
        final_novel = json.load(file)
    novel_file_path = os.path.join(folder_path, 'novel.txt')
    with open(novel_file_path, 'w', encoding='utf-8') as file:
        for page in final_novel:
            file.write(
                f"Page {page['page_id']}, Chapter {page['chapter_id']}\n\n{page['text']}\n\n")
    print("The novel has been successfully written to 'novel.txt'")
    return

def divide_into_chunks(text):
    """This function divides the text into chunks of up to 1000 words."""
    return textwrap.wrap(text, 1000)

def divide_into_parts(text):
    """This function divides the text into parts based on the pipe character."""
    return text.split('|')

if __name__ == "__main__":
    generate_novel()

#path agents/story_teller_02.py
