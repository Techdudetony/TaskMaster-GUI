import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import TaskMasterApp

def main():
    app = QApplication(sys.argv)
    window = TaskMasterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
