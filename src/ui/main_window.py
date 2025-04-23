from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QSize
from logic.task import Task
from logic.storage import load_tasks, save_tasks
from logic.utils import style_task_item
from ui.dialogs import AddTaskDialog

class TaskMasterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Master GUI")
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QListWidget {
                border: none;
                background-color: #ffffff;
            }
            QListWidget::item {
                padding: 12px;
                margin: 6px 0;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
            QListWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 10px;
                background-color: #f0f0f0;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)
        self.setMinimumWidth(600)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("👑 <span style='font-size: 20px;'>Task Master</span>")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            background-color: #f9f9f9;
            font-weight: bold;
            font-size: 22px;
            padding: 16px;
            margin-bottom: 15px;
            border-radius: 12px;
            border: 1px solid #eaeaea;
        """)
        
        # Task List
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)
        self.task_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.task_list.currentRowChanged.connect(self.update_complete_button_text)
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
        btn_edit = QPushButton("✏️ Edit Task")
        self.btn_complete = QPushButton("✅ Mark Complete")
        btn_delete = QPushButton("❌ Delete Task")
        
        for btn in [btn_edit, self.btn_complete, btn_delete]:
            btn.setMinimumHeight(35)
            layout.addWidget(btn)
          
        # Create the inner layout container (frame)  
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }                        
        """)
        container.setLayout(layout)
        
        #Apply drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80)) # soft black shadow
        container.setGraphicsEffect(shadow)
        
        # Add to an outer layout and apply to the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(container)
        self.setLayout(main_layout)

        # Floating Action Button
        self.fab = QPushButton("+")
        self.fab.setFixedHeight(48)
        self.fab.setMinimumSize(48, 48)
        self.fab.setMaximumSize(140, 48)  # Allow room for expansion
        self.fab.resize(48, 48)
        self.fab.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 20px;
                border-radius: 24px;
                padding: 0px 16px; /* Top-Bottom, Left-Right */
                text-align: center;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
            QPushButton:pressed {
                background-color: #004a82;
            }
        """)

        self.fab.clicked.connect(self.open_add_task_dialog)

        # Manually position FAB (overlay)
        self.fab.setParent(self)
        self.fab.move(self.width() - 70, self.height() - 70)
        self.fab.show()
        
        from PyQt6.QtCore import QPropertyAnimation

        # Animation for expanding FAB
        self.fab_animation = QPropertyAnimation(self.fab, b"size")
        self.fab_animation.setDuration(250)

        self.fab.enterEvent = self.expand_fab
        self.fab.leaveEvent = self.collapse_fab

        # Ensure it stays in position on resize
        self.resizeEvent = self._on_resize
        
        btn_edit.clicked.connect(self.open_edit_task_dialog)
        self.btn_complete.clicked.connect(self.toggle_task_completion)
        btn_delete.clicked.connect(self.delete_selected_task)
        
        # Load and display tasks
        self.tasks = load_tasks()
        for task in self.tasks:
            checkbox = '✔' if task.completed else ' '
            display = f"[{checkbox}] {task.title} (Priority: {task.priority}, Due: {task.due_date})"
            list_item = QListWidgetItem(display)
            self.task_list.addItem(list_item)
            style_task_item(list_item, task)
            
    def _on_resize(self, event):
        self.fab.move(22, self.height() - 70)
        
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
        self.update_complete_button_text()
        
    def update_complete_button_text(self):
        selected_row = self.task_list.currentRow()
        if selected_row < 0:
            self.btn_complete.setText("✅ Mark Complete")
            return

        task = self.tasks[selected_row]
        if task.completed:
            self.btn_complete.setText("↩️ Unmark Complete")
        else:
            self.btn_complete.setText("✅ Mark Complete")
            
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

    def expand_fab(self, event):
        self.fab.setText("+ Add Task")
        self.fab_animation.stop()
        self.fab_animation.setStartValue(self.fab.size())
        self.fab_animation.setEndValue(QSize(140, 48))
        self.fab_animation.start()

    def collapse_fab(self, event):
        try:
            self.fab_animation.finished.disconnect(self._reset_fab_text)
        except TypeError:
            pass  # not connected yet
        self.fab_animation.stop()
        self.fab_animation.setStartValue(self.fab.size())
        self.fab_animation.setEndValue(QSize(48, 48))
        self.fab_animation.finished.connect(self._reset_fab_text)
        self.fab_animation.start()
        
    def _reset_fab_text(self):
        self.fab.setText("+")
        self.fab_animation.finished.disconnect(self._reset_fab_text)
