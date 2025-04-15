# Handles saving and loading tasks to/from a JSON file

import json
import os
from .task import Task

# Path to the JSON file in the data directory
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tasks.json")

def load_tasks():
    '''
    Load tasks from the JSON file.
    Returns a list of Task objects.
    '''
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            return [Task.from_dict(t) for t in data]
        except json.JSONDecodeError:
            # Return empty list if the file is corrupt or empty
            return []
        
def save_tasks(tasks):
    '''
    Save a list of Task objects to the JSON file.
    '''
    with open(DATA_FILE, "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2)
        
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)