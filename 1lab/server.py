import socket
import threading
import os
import json
import struct
import tempfile
import logging
from pydub import AudioSegment

HOST = "127.0.0.1"
PORT = 5000
AUDIO_DIR = "audio_files"
METADATA_FILE = "audio_metadata.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def update_metadata():
    metadata = []
    for filename in os.listdir(AUDIO_DIR):
        if filename.endswith((".mp3", ".wav")):
            path = os.path.join(AUDIO_DIR, filename)
            audio = AudioSegment.from_file(path)
            metadata.append({
                "filename": filename,
                "duration": len(audio) // 1000,
                "format": filename.split('.')[-1]
            })
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def handle_client(conn, addr):
    logging.info(f"Клиент подключен: {addr}")
    try:
        data = conn.recv(1024).decode("utf-8")
        if data == "LIST":
            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                metadata = f.read()
            conn.sendall(metadata.encode("utf-8"))

        elif data.startswith("GET"):
            _, filename, start, end = data.split("|")
            start = int(start) * 1000
            end = int(end) * 1000
            full_path = os.path.join(AUDIO_DIR, filename)
            audio = AudioSegment.from_file(full_path)
            segment = audio[start:end]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                segment.export(temp_file.name, format="mp3")
                temp_file_path = temp_file.name

            with open(temp_file_path, "rb") as f:
                audio_data = f.read()
            os.remove(temp_file_path)

            conn.sendall(struct.pack("!I", len(audio_data)))
            conn.sendall(audio_data)
        else:
            conn.sendall("Неверная команда".encode("utf-8"))
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        conn.close()

def start_server():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    update_metadata()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()