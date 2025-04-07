import threading
import time
import server
import client

def run_server():
    server.start_server()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(1)  # Ждем, пока сервер поднимется

def main():
    while True:
        print("\nКоманды:")
        print("1 — Показать список аудиофайлов")
        print("2 — Скачать фрагмент аудиофайла")
        print("3 — Выйти")
        cmd = input("Введите команду: ")

        if cmd == "1":
            client.send_request("LIST")
        elif cmd == "2":
            fname = input("Имя файла: ")
            start = input("Начало (сек): ")
            end = input("Конец (сек): ")
            client.send_request(f"GET|{fname}|{start}|{end}")
        elif cmd == "3":
            print("Завершение работы...")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()
