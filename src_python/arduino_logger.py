import serial
import time
import cv2

usb_camera = 1
camera = cv2.VideoCapture(usb_camera)
photoCounter = 0

# Настройки последовательного порта
serial_port = 'COM5'  # Замените на порт, к которому подключено Arduino
baud_rate = 9600             # Скорость передачи данных
output_file = 'data_log.txt' # Имя файла для записи

# Значения показаний акселерометра
x = []
t = []

start_time = time.time()


try:
    # Открываем соединение с Arduino
    with serial.Serial(serial_port, baud_rate, timeout=1) as arduino, open(output_file, 'w') as file:
        print("Чтение данных началось. Нажмите Ctrl+C для выхода.")
        
        while True:
            # Читаем строку данных от Arduino
            data = arduino.readline().decode('utf-8').strip().split()
            if data:
                if data[0] == 'P':
                    try:
                        ret, frame = camera.read()
                    except Exception as e:
                        print("Ошибка чтения с камеры: {e}")
                        continue
                    photoCounter += 1
                    print("Снимок!")
                    try:
                        cv2.imwrite(f"microscope-{photoCounter}.png", frame)
                    except Exception as e:
                        print("Ошибка записи фото: {e}")
                    continue
                elif data[0].lstrip('-').isnumeric():
                    current_time = time.time() - start_time
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