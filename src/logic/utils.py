# Provides helper functions such as sorting logic, overdue checks, and GUI item styling
from datetime import datetime
from PyQt6.QtGui import QColor

# Priority levels used across app
PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

# Priority-to-color mapping
PRIORITY_COLORS = {
    "Critical": "#8B0000",  # Dark Red
    "High": "#FF8C00",      # Orange
    "Medium": "#1E90FF",    # Dodger Blue
    "Low": "#228B22",       # Forest Green
}

def sort_tasks(tasks, by="priority"):
    '''
    Sort tasks by priority or due date.
    
    Parameters:
        tasks: list of Task objects
        by: sorting key ('priority' or 'due_date')
        
    Returns:
        Sorted list of Task objects
    '''
    if by == "priority":
        # Define custom priority order
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        return sorted(tasks, key=lambda t: priority_order.get(t.priority, 4))
    elif by == "due_date":
        # Use due date string (or empty string if None)
        return sorted(tasks, key=lambda t: t.due_date or "")
    else:
        return tasks
    
def get_priority_color(priority: str) -> str:
    '''Return the hex color code for a given priority level.'''
    return PRIORITY_COLORS.get(priority, "black")

def is_task_overdue(task) -> bool:
    '''Return True if the task's due date is before today.'''
    try:
        if task.due_date:
            if isinstance(task.due_date, str):
                due = datetime.strptime(task.due_date.strip(), "%Y-%m-%d").date()
            elif isinstance(task.due_date, datetime):
                due = task.due_date.date()
            else:
                due = task.due_date  # assume already a date object
            return due < datetime.now().date()
    except Exception as e:
        print(f"[Overdue Error] {task.title}: {e}")
    return False

from PyQt6.QtCore import Qt

def style_task_item(item, task):
    '''
    Style a QListWidgetItem with:
    - emoji prefix if overdue
    - colored text based on priority
    '''
    text = item.text()
    
    if is_task_overdue(task):
        print(f"[OVERDUE] {task.title} - Due: {task.due_date}")
        item.setText(f"⚠️ {text}")  # prefix indicator emoji
        item.setData(Qt.ItemDataRole.UserRole, "overdue")  # for possible future use

    # Color code by priority
    item.setForeground(QColor(get_priority_color(task.priority)))
