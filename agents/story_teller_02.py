"""this module is used to generate a novel based on a seed text."""

import os
import json
import textwrap
import openai
from langchain.chat_models.openai import ChatOpenAI
import config


def generate_novel(seed_text):
    """This function generates a novel based on a seed text."""
    # Initialize llm
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                     max_tokens=config.OPENAI_MAX_TOKENS,
                     api_key=config.OPENAI_API_KEY, streaming=True)
    prompt_text = f"""
     Stage 1
        Create a outline for a novel based on this {seed_text}.  
        The novel is set in (insert) setting.
        The main character is (insert) main character.
        The main character's goal is to (insert) goal.
        The main character's obstacles are (insert) obstacles.
        The main character's allies are (insert) allies.
        The main character's enemies are (insert) enemies.
        The novel ends with (insert) ending.
        Here is an example of how this prompt template could be used to 
        generate a plot for a novel based on the seed text "A young woman 
        travels to a faraway land in search of a cure for her dying father."
        The novel is set in a medieval fantasy world.
        The main character is a young woman named Anya.
        Anya's goal is to find a cure for her dying father.
        Anya's obstacles are the dangers of the journey,
        the evil forces that are trying to stop her,
        and her own doubts and fears.
        Anya's allies are her friends and family,
        the people she meets along the way, and her own inner strength.
        Anya's enemies are the evil forces that are trying to stop her,
        and her own doubts and fears.
        The novel ends with Anya finding a cure for her father and saving his life.
    Stage 2 
        Utilizing the response from above as seed text...create a detailed plot for a novel.
        De-limit the plot with a new line to idicate when new part should start to the novel.
    """

    # File Storage location
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, 'broad_plot.json')

    # Step 1: Generate a broad plot
    broad_plot = llm.call_as_llm(prompt_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(broad_plot, file)
    print("The broad plot has been successfully written to 'broad_plot.json")

    # Step 2: Iterate through plot in chunks, giving it more depth
    with open(file_path, 'w', encoding='utf-8') as file:
        broad_plot = json.load(file)
    detailed_plot = []
    part_id = 0
    for chunk in divide_into_parts(broad_plot):
        parts = llm.call_as_llm(f"""
        You're a novelist, create a more detailed and descriptive version of:
        {chunk},
        """)
        detailed_plot.append({"part_id": part_id, "text": parts})
        part_id += 1
    detail_file_path = os.path.join(dir_path, 'detailed_plot.json')
    with open(detail_file_path, 'w', encoding='utf-8') as file:
        json.dump(detailed_plot, file)
    print("The detailed plot has been successfully written to 'detailed_plot.json")

    # Step 3: Iterate through detailed plot, creating descriptive scenes
    with open(detail_file_path, 'w', encoding='utf-8') as file:
        detailed_plot = json.load(file)
    scene_descriptions = []
    chapter_id = 0
    for part in detailed_plot:
        plot_point = part["text"]
        scene_prompt = f"""
        You're a novelist, create a more detailed and descriptive version of:
        {plot_point}
        """
        scene = llm.call_as_llm(scene_prompt)
        scene_descriptions.append(
            {"chapter_id": chapter_id, "text": scene, "part_id": part["part_id"]})
        chapter_id += 1
    scene_file_path = os.path.join(dir_path, 'scene_descriptions.json')
    with open(scene_file_path, 'w', encoding='utf-8') as file:
        json.dump(scene_descriptions, file)
    print("The scene descriptions have been successfully written to 'scene_descriptions.json'")

    # Step 4: Iterate through each scene, creating final, beautifully descriptive scenes
    with open(scene_file_path, 'w', encoding='utf-8') as file:
        scene_descriptions = json.load(file)
    final_novel = []
    page_id = 0
    for chapter in scene_descriptions:
        scene = chapter["text"]
        final_edit_prompt = f"""
        You're a novelist, create a more detailed and descriptive version of:
        {scene}
        """
        final_edit = llm.call_as_llm(final_edit_prompt)
        final_novel.append(
            {"page_id": page_id, "text": final_edit, "chapter_id": chapter["chapter_id"]})
        page_id += 1
    final_file_path = os.path.join(dir_path, 'final_novel.json')
    with open(final_file_path, 'w', encoding='utf-8') as file:
        json.dump(final_novel, file)

    # Write final novel to a text file
    with open(final_file_path, 'w', encoding='utf-8') as file:
        final_novel = json.load(file)
    novel_file_path = os.path.join(dir_path, 'novel.txt')
    with open(novel_file_path, 'w', encoding='utf-8') as file:
        for page in final_novel:
            file.write(
                f"Page {page['page_id']}, Chapter {page['chapter_id']}\n\n{page['text']}\n\n")

    print("The novel has been successfully written to 'novel.txt'")
    return

# Helper function to divide text into manageable chunks


def divide_into_chunks(text):
    """This function divides the text into chunks of up to 400 words."""
    return textwrap.wrap(text, 400)


def divide_into_parts(text):
    """This function divides the text into parts based on new lines."""
    return text.split('\n')


if __name__ == "__main__":
    INPUT_TEXT = """
        The guardinals have no record of their origin. They have been
the protectors of Elysium for all of the plane’s recorded history.
For as long as Elysium has known the guardinals, there have
been the Celestial Lion and his Five Companions, exemplars
and epitomes of their respective kind.
"""
    generate_novel(INPUT_TEXT)

#path agents/story_teller_02.py