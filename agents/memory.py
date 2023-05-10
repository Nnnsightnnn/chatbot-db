"""this module is responsible for storing and retrieving memories"""
import json
from datetime import datetime

class Memory:
    """this class is responsible for storing and retrieving memories"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """load data from file"""
        try:
            with open(self.file_path, 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        """save data to file"""
        with open(self.file_path, 'w', encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def add_memory(self, user_message, response):
        """add a memory to the data"""
        current_time = str(datetime.now())
        memory = {
            'user_message': user_message,
            'response': response,
            'time': current_time
        }
        self.data.append(memory)
        self.save_data()

    def get_memories(self):
        """return all memories"""
        return self.data

    def retrieve_memory(self, index):
        """retrieve a memory by index"""
        if 0 <= index < len(self.data):
            return self.data[index]
        else:
            return None

    def get_memory_count(self):
        """return the number of memories"""
        unique_entries = set((entry['user_message'], entry['response']) for entry in self.data)
        return len(unique_entries)

# Path: agents/memory.py
