import socket
import struct
import json
import os
import logging

HOST = "127.0.0.1"
PORT = 5000
SAVE_DIR = "received_files"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
os.makedirs(SAVE_DIR, exist_ok=True)

def send_request(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(command.encode("utf-8"))

        if command == "LIST":
            response = client.recv(4096)
            files = json.loads(response.decode("utf-8"))
            logging.info("Доступные аудиофайлы:")
            for file in files:
                print(f"{file['filename']} ({file['duration']} сек) [{file['format']}]")

        elif command.startswith("GET"):
            raw_size = client.recv(4)
            if not raw_size:
                logging.error("Нет данных")
                return
            size = struct.unpack("!I", raw_size)[0]
            audio_data = b""
            while len(audio_data) < size:
                part = client.recv(4096)
                if not part:
                    break
                audio_data += part

            filename = command.split("|")[1]
            output_file = os.path.join(SAVE_DIR, f"received_{filename}")
            with open(output_file, "wb") as f:
                f.write(audio_data)
            logging.info(f"Аудиофайл сохранен как {output_file}")