import os, sys
from PyQt6 import QtWidgets
from main_window import MainWindow

def main():
    application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)
    print(f"Рабочая директория: {os.getcwd()}")

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
