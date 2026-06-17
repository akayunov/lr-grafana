import asyncio
import os
import pickle
import struct


async def handle_carbon_pickle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Асинхронный обработчик бинарных Pickle-данных от lr-carbon-aggregator-aggregator."""
    peer = writer.get_extra_info("peername")
    print(f"[*] Новое соединение (Pickle) от агрегатора: {peer}", flush=True)

    try:
        while True:
            # 1. Читаем заголовок (4 байта), содержащий длину сообщения
            header = await reader.readexactly(4)
            if not header:
                break

            # Декодируем длину пакета (!I = Big-Endian unsigned int)
            payload_len = struct.unpack("!I", header)[0]

            # 2. Читаем бинарное тело пакета на основе полученной длины
            payload = await reader.readexactly(payload_len)

            # 3. Десериализуем данные из формата Pickle
            # Данные приходят списком кортежей: [(metric_name, (timestamp, value)), ...]
            datapoints = pickle.loads(payload)

            # 4. Выводим полученные метрики на экран
            for metric_name, (timestamp, value) in datapoints:
                print(f"[Pickle] {metric_name} = {value} (Time: {timestamp})", flush=True)
                # if not metric_name.startswith("carbon.aggregator."):
                #     with open('/app/metric_storage', 'a') as f:
                #         f.write(f"[Pickle] {metric_name} = {value} (Time: {timestamp})\n")
                if not metric_name.startswith("carbon.aggregator."):
                    with open("/app/metric_storage", "a") as f:
                        f.write(
                            f"[Pickle] {metric_name} = {value} (Time: {timestamp})\n"
                        )
                        f.flush()  # Очищает буфер Python
                        os.fsync(f.fileno())  # Принудительно сбрасывает кэш ОС на диск

    except asyncio.IncompleteReadError:
        print(f"[-] Агрегатор {peer} закрыл соединение.", flush=True)
    except Exception as e:
        print(f"[!] Ошибка при обработке Pickle: {e}", flush=True)
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[*] Соединение с {peer} успешно закрыто.", flush=True)


async def main():
    # Запускаем TCP-сервер на порту 2004 (стандартный порт для Pickle в Graphite)
    server = await asyncio.start_server(handle_carbon_pickle, "0.0.0.0", 2004)

    # Исправленный синтаксис получения адреса сокета для Python 3.14+
    if server.sockets:
        # Извлекаем первый сокет из кортежа и вызываем getsockname у него
        addr = server.sockets[0].getsockname()
        print(f"[*] Имитатор lr-carbon-aggregator-cache запущен и слушает Pickle на {addr}", flush=True)
    else:
        print("[*] Сервер запущен, но сетевые сокеты не инициализированы.", flush=True)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Сервер остановлен пользователем.", flush=True)
