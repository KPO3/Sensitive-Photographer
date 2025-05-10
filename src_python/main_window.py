from PyQt6 import QtWidgets
import cv2, subprocess, sys, os
from ui_mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.refresh_cameras()
        self.setup_connections()

        self.logger_process = None 
        self.graph_process = None

    def setup_connections(self):
        self.ui.StartBtn.clicked.connect(self.start)
        self.ui.GraphBtn.clicked.connect(self.graph)
        
    def start(self):
        if self.logger_process == None:
            print("Логгер запущен")
            self.ui.StartBtn.setText("Стоп")
            process_args = [self.ui.PortLineEdit.text(), self.ui.CameraComboBox.currentText(), self.ui.NameLineEdit.text()]
            self.logger_process = subprocess.Popen([sys.executable, "arduino_logger.py", *process_args])
        else:
            self.logger_process.terminate()
            self.logger_process = None
            print("Логгер остановлен")
            self.ui.StartBtn.setText("Запуск")

    def graph(self):
        if self.graph_process == None:
            print("График создан")
            self.ui.GraphBtn.setText("Стоп график")
            self.graph_process = subprocess.Popen([sys.executable, "qtgrapher.py", self.ui.NameLineEdit.text()])
        else:
            self.ui.GraphBtn.setText("График")
            self.graph_process.terminate()
            self.graph_process = None
            print("График остановлен")


    def get_available_cameras(self):
        available_cameras = []
        dev_port = 0
        backend = (
            cv2.CAP_DSHOW if os.name == 'nt' else  # Windows
            cv2.CAP_V4L2 if os.name == 'posix' else  # Linux
            cv2.CAP_ANY  # macOS/другие
        )
        while True:
            cap = cv2.VideoCapture(dev_port, backend)
            if not cap.isOpened():
                break
            available_cameras.append(dev_port)
            cap.release()
            dev_port += 1
            print(f"Обнаружил камеру {dev_port}")
        return available_cameras

    def refresh_cameras(self):
        self.ui.CameraComboBox.clear()
        available_cameras = self.get_available_cameras()
        
        if not available_cameras:
            self.ui.CameraComboBox.addItem("Не найдено доступных камер")
            self.ui.CameraComboBox.setEnabled(False)
        else:
            for cam_idx in available_cameras:
                self.ui.CameraComboBox.addItem(f"Камера {cam_idx}", cam_idx)

    def closeEvent(self, event):
        if self.logger_process is not None:
            self.logger_process.terminate()
            self.logger_process.wait()
        if self.graph_process is not None:
            self.graph_process.terminate()
            self.graph_process.wait()
        super().closeEvent(event)
