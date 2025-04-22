import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox,
    QLineEdit, QComboBox, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QListWidgetItem
)
from PyQt6.QtCore import Qt, QDate

from logic.storage import load_tasks, save_tasks
from logic.task import Task
from logic.utils import style_task_item  # Modular styling logic

class TaskMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Master GUI")
        self.setMinimumWidth(600)
        self.setStyleSheet("font-family: Arial; font-size: 14px;")
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("👑 Task Master")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Task List
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)
        self.task_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.task_list.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)
        self.task_list.setStyleSheet("""
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #e6f2ff;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
        """)

        # Buttons
        btn_add = QPushButton("➕ Add Task")
        btn_edit = QPushButton("✏️ Edit Task")
        btn_complete = QPushButton("✅ Mark Complete")
        btn_delete = QPushButton("❌ Delete Task")
        
        for btn in [btn_add, btn_edit, btn_complete, btn_delete]:
            btn.setMinimumHeight(35)
            layout.addWidget(btn)
            
        self.setLayout(layout)
        
        btn_add.clicked.connect(self.open_add_task_dialog)
        btn_edit.clicked.connect(self.open_edit_task_dialog)
        btn_complete.clicked.connect(self.toggle_task_completion)
        btn_delete.clicked.connect(self.delete_selected_task)
        
        # Load and display tasks
        self.tasks = load_tasks()
        for task in self.tasks:
            checkbox = '✔' if task.completed else ' '
            display = f"[{checkbox}] {task.title} (Priority: {task.priority}, Due: {task.due_date})"
            list_item = QListWidgetItem(display)
            self.task_list.addItem(list_item)
            style_task_item(list_item, task)
        
    def show_popup(self, message):
        QMessageBox.information(self, "Action", message)
        
    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            new_id = max([t.id for t in self.tasks], default=0) + 1
            new_task = Task(
                id=new_id,
                title=data["title"],
                priority=data["priority"],
                due_date=data["due_date"]
            )
            self.tasks.append(new_task)
            save_tasks(self.tasks)

            checkbox = "✔" if new_task.completed else " "
            display = f"[{checkbox}] {new_task.title} (Priority: {new_task.priority}, Due: {new_task.due_date})"
            list_item = QListWidgetItem(display)
            self.task_list.addItem(list_item)
            style_task_item(list_item, new_task)
        
    def open_edit_task_dialog(self):
        selected_row = self.task_list.currentRow()
        if selected_row < 0:
            self.show_popup("Please select a task to edit.")
            return
        
        task = self.tasks[selected_row]
        dialog = AddTaskDialog(self, task)
        if dialog.exec():
            data = dialog.get_data()
            task.title = data["title"]
            task.priority = data["priority"]
            task.due_date = data["due_date"]
            save_tasks(self.tasks)
            self.refresh_task_list()
            
    def toggle_task_completion(self):
        selected_row = self.task_list.currentRow()
        if selected_row < 0:
            self.show_popup("Please select a task to mark as complete.")
            return

        task = self.tasks[selected_row]
        task.completed = not task.completed
        save_tasks(self.tasks)
        self.refresh_task_list()
            
    def delete_selected_task(self):
        selected_row = self.task_list.currentRow()
        if selected_row < 0:
            self.show_popup("Please select a task to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            self.tasks.pop(selected_row)
            save_tasks(self.tasks)
            self.refresh_task_list()
            
    def refresh_task_list(self):
        self.task_list.clear()
        for task in self.tasks:
            checkbox = "✔" if task.completed else " "
            display = f"[{checkbox}] {task.title} (Priority: {task.priority}, Due: {task.due_date})"
            list_item = QListWidgetItem(display)
            self.task_list.addItem(list_item)
            style_task_item(list_item, task)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task" if task is None else "Edit Task")
        self.setFixedSize(300, 200)
        
        layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Critical", "High", "Medium", "Low"])
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        
        if task:
            self.title_input.setText(task.title)
            index = self.priority_input.findText(task.priority)
            self.priority_input.setCurrentIndex(index)
            self.due_date_input.setDate(QDate.fromString(task.due_date, "yyyy-MM-dd"))
        
        layout.addRow("Title: ", self.title_input)
        layout.addRow("Priority: ", self.priority_input)
        layout.addRow("Due Date: ", self.due_date_input)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        
    def get_data(self):
        return {
            "title": self.title_input.text(),
            "priority": self.priority_input.currentText(),
            "due_date": self.due_date_input.date().toString("yyyy-MM-dd")
        }

def main():
    app = QApplication(sys.argv)
    window = TaskMasterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
