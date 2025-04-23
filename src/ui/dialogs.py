from PyQt6.QtWidgets import (
    QDialog, QLineEdit, QComboBox, QDateEdit, QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import QDate

class AddTaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task" if task is None else "Edit Task")
        self.setFixedSize(300, 200)
        
        layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Critical", "High", "Medium", "Low"])
        self.tag_input = QComboBox()
        self.tag_input.addItems(["None", "Work", "School", "Personal"])
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
        layout.addRow("Tag: ", self.tag_input)
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
            "tag": self.tag_input.currentText() if self.tag_input.currentText() != "None" else None,
            "due_date": self.due_date_input.date().toString("yyyy-MM-dd")
        }
