# Defines the Task class with attributes and seriaalization logic

from colorama import Fore, Style, init
from datetime import datetime
init(autoreset=True)

class Task:
    def __init__(self, id, title, due_date=None, priority="Low", completed=False, tag=None):
        # Unique task ID, title, due date, priority level, and completion status
        self.id = id
        self.title = title
        self.due_date = due_date
        self.priority= priority
        self.completed= completed
        self.tag= tag
        
    def to_dict(self):
        '''Convert the task object to a dictionary for JSON serialization'''
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed,
            "tag": self.tag
        }
        
    @staticmethod
    def from_dict(data):
        '''Create a Task object from a disctionary (used when loading from JSON)'''
        return Task(
            id=data["id"],
            title=data["title"],
            due_date=data.get("due_date"),
            priority=data.get("priority", "Low"),
            completed=data.get("completed", False),
            tag=data.get("tag")
        )
        
    def __str__(self):
        '''Return a formatted string representation of the task.'''
        # Priority Colors
        color_map = {
            "Critical": Fore.RED,
            "High": Fore.YELLOW,
            "Medium": Fore.CYAN,
            "Low": Fore.GREEN
        }
        priority_color = color_map.get(self.priority, Fore.WHITE)
        
        # Overdue check
        overdue = False
        if self.due_date:
            try:
                due_date_obj = datetime.strptime(self.due_date, "%Y-%m-%d")
                if due_date_obj < datetime.now():
                    overdue = True
            except ValueError:
                pass # Invalid date format won't break rendering
            
        due_display = f"{Fore.RED}{self.due_date}{Style.RESET_ALL}" if overdue else self.due_date
        tag_display = f" [Tag: {self.tag}]" if self.tag else ""
        checkbox = '✔' if self.completed else ' '
        
        return f"[{checkbox}] {self.id}: {self.title} ({priority_color}Priority: {self.priority}{Style.RESET_ALL}, Due: {due_display}{tag_display})"