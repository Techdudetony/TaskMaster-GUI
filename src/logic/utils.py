# Provides helper functions such as sorting logic

PRIORITY_LEVELS = ["Critical", "High", "Medium", "Low"]

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