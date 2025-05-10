import sys
import pyqtgraph as pg
import os
from PyQt6 import QtCore, QtWidgets

class RealTimePlot:
    def __init__(self, filename):
        self.filename = filename

        # Создаем приложение и окно
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = QtWidgets.QMainWindow()
        self.win.setWindowTitle('График данных датчика')

        # Создаем PlotWidget
        self.plot_widget = pg.PlotWidget()
        self.win.setCentralWidget(self.plot_widget)
        self.win.show()

        # Настройка графика
        self.plot_widget.setLabel('left', 'Y')
        self.plot_widget.setLabel('bottom', 'X')
        self.curve = self.plot_widget.plot(pen='y')

        # Данные для графика
        self.data_x = []
        self.data_t = []

        # Таймер для обновления графика
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # Обновление каждые 50 мс

    def update(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if lines:
                    # Предполагаем, что данные в файле разделены пробелами или запятыми
                    # и каждая строка содержит два значения: x и t
                    x, t = map(float, lines[-1].strip().split())
                    self.data_x.append(x)
                    self.data_t.append(t)

                    # Ограничиваем количество точек на графике, чтобы не перегружать память
                    if len(self.data_x) > 1000:
                        self.data_x.pop(0)
                        self.data_t.pop(0)

                    # Обновляем график
                    self.curve.setData(self.data_t, self.data_x)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
        except KeyboardInterrupt:
            print("\nГрафик остановлен пользователем.")
    def exit(self):
        print("График закрыт")

    def run(self):
        sys.exit(self.app.exec())

if __name__ == '__main__':
    filename = 'data_log.txt'  # Укажите путь к вашему файлу с данными
    if len(sys.argv) > 1:
        filename = sys.argv[1] + '.txt'
    print(f"Читаю из {filename}")
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), sys.argv[1], filename)
    plot = RealTimePlot(filepath)
    plot.run()
