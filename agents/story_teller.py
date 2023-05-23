import textwrap
import openai
import os
from langchain.chat_models.openai import ChatOpenAI 
import config

def generateNovel(seed_text):
    # Initialize llm
    seed_text = f"""
    """
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
        De-limit each plot point with a new line to idicate a new part to the novel.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(temperature=config.OPENAI_TEMPERATURE, model_name='gpt-3.5-turbo',
                     max_tokens=config.OPENAI_MAX_TOKENS, api_key=config.OPENAI_API_KEY, streaming=True)

    # Step 1: Generate a broad plot
    broad_plot = llm.call_as_llm(prompt_text)

    # Step 2: Iterate through plot in chunks, giving it more depth
    detailed_plot = []
    part_id = 0
    for chunk in divideIntoParts(broad_plot):
        parts = llm.call_as_llm(f"""
        You're a novelist, create a more detailed and descriptive version of:
        {chunk},
        """)
        detailed_plot.append({"part_id": part_id, "text": parts})
        part_id += 1


# Step 3: Iterate through detailed plot, creating descriptive scenes
    scene_descriptions = []
    chapter_id = 0
    for part in detailed_plot:
        plot_point = part["text"]
        scene_prompt = f"""
        You're a novelist, create a more detailed and descriptive version of:
        {plot_point}
        """
        scene = llm.call_as_llm(scene_prompt)
        scene_descriptions.append({"chapter_id": chapter_id, "text": scene, "part_id": part["part_id"]})
        chapter_id += 1


# Step 4: Iterate through each scene, creating final, beautifully descriptive scenes
    final_novel = []
    page_id = 0
    for chapter in scene_descriptions:
        scene = chapter["text"]
        final_edit_prompt = f"""
        You're a novelist, create a more detailed and descriptive version of:
        {scene}
        """
        final_edit = llm.call_as_llm(final_edit_prompt)
        final_novel.append({"page_id": page_id, "text": final_edit, "chapter_id": chapter["chapter_id"]})
        page_id += 1

        # Write final novel to a text file
    with open('novel.txt', 'w') as f:
        for page in final_novel:
            f.write(f"Page {page['page_id']}, Chapter {page['chapter_id']}\n\n{page['text']}\n\n")

    print("The novel has been successfully written to 'novel.txt'")
    return final_novel


# Helper function to divide text into manageable chunks
def divideIntoChunks(text):
    # This function divides the text into chunks of up to 400 words.
    return textwrap.wrap(text, 400)

def divideIntoParts(text):
    # This function divides the text into parts based on new lines.
    return text.split('\n')

if __name__ == "__main__":
    seed_text = input(f"""
    The guardinals have no record of their origin. They have been
the protectors of Elysium for all of the plane’s recorded history.
For as long as Elysium has known the guardinals, there have
been the Celestial Lion and his Five Companions, exemplars
and epitomes of their respective kind. 
""")
    generateNovel(seed_text)