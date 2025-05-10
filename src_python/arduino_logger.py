import serial
import time
import cv2
import sys
import os

# Входные параметры argv:
# argv[1] - порт Arduino
# argv[2] - id камеры
# argv[3] - имя файла и папки для записи данных графика

def read_data():
    # Настройки последовательного порта
    serial_port = 'COM5' 
    if len(sys.argv) > 1:
        print(f"Используем порт {sys.argv[1]}")
        serial_port = sys.argv[1]

    # Настройки камеры
    usb_camera = 1
    camera = cv2.VideoCapture(usb_camera)
    if len(sys.argv) > 2:
        print(f"Используем камеру {sys.argv[2]}")
        usb_camera = sys.argv[2]

    # Настройки файла для записи данных
    output_file = 'data_log.txt' # Имя файла для записи
    if len(sys.argv) > 3:
        output_file = sys.argv[3] + '.txt'
        print(f"Записываем данные в файл {output_file}")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(current_dir, sys.argv[3])
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)

    baud_rate = 9600             # Скорость передачи данных

    # Значения показаний акселерометра
    x = []
    t = []

    photoCounter = 0
    start_time = time.time()

    try:
        # Открываем соединение с Arduino
        with serial.Serial(serial_port, baud_rate, timeout=1) as arduino, open(output_file, 'w') as file:
            print("Чтение данных началось. Нажмите Ctrl+C для выхода.")
            
            while True:
                # Читаем строку данных от Arduino
                data = arduino.readline().decode('utf-8').strip().split()
                if data:
                    current_time = time.time() - start_time
                    if data[0] == 'P':
                        try:
                            ret, frame = camera.read()
                        except Exception as e:
                            print(f"Ошибка чтения с камеры: {e}")
                            continue
                        photoCounter += 1
                        print("Снимок!")
                        try:
                            cv2.imwrite(f"microscope-{photoCounter}-{round(current_time, 2)}.png", frame)
                        except Exception as e:
                            print(f"Ошибка записи фото: {e}")
                        continue
                    elif data[0].lstrip('-').isnumeric():
                        print(f"x: {data[0]} - t: {current_time}")

                        x.append(int(data[0]))
                        t.append(current_time)

                        file.write(f"{data[0]} {current_time}\n")  # Записываем данные в файл
                        file.flush()             # Принудительно записываем данные на диск
    except serial.SerialException as e:
        print(f"Ошибка подключения к {serial_port}: {e}")
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    read_data()
