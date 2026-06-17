import socket
import time


def send(metrics, host="carbon-aggregator", port=2023):
    try:
        # Создание TCP-сокета
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # Отправка данных в кодировке ASCII
            for metric_name, metric_value, timestamp in metrics:
                # metric_name = "tests-lr-carbon-aggregator.metric.1"
                # metric_value = "4"
                timestamp = timestamp or int(time.time())
                # Сборка строки (обязательно с символом новой строки в конце)
                payload = f"{metric_name} {metric_value} {timestamp}\n"
                s.sendall(payload.encode("ascii"))
            # Закрытие сокета на запись (аналог флага nc -N)
            s.shutdown(socket.SHUT_WR)
        print("Метрика успешно отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке метрики: {e}")
