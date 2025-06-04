from celery import Celery
import time
from app.websocket.websocket_manager import websocket_manager
import json
import asyncio
from app.services.encode_service import encode_text, decode_text


app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def async_encode(text: str, key: str, task_id: str, user_id: str):
    asyncio.run(send_progress(task_id, user_id, 0))
    result = encode_text(text, key)
    time.sleep(2)
    asyncio.run(send_progress(task_id, user_id, 50))
    time.sleep(2)
    asyncio.run(send_progress(task_id, user_id, 100))
    asyncio.run(websocket_manager.broadcast_completion(task_id, user_id, result))
    return result

@app.task
def async_decode(encoded_data: str, key: str, huffman_codes: dict, padding: int, task_id: str, user_id: str):
    asyncio.run(send_progress(task_id, user_id, 0))
    result = decode_text(encoded_data, key, huffman_codes, padding)
    time.sleep(2)
    asyncio.run(send_progress(task_id, user_id, 50))
    time.sleep(2)
    asyncio.run(send_progress(task_id, user_id, 100))
    asyncio.run(websocket_manager.broadcast_completion(task_id, user_id, {"decoded_text": result}))
    return {"decoded_text": result}

async def send_progress(task_id: str, user_id: str, progress: int):
    await websocket_manager.broadcast_progress(task_id, user_id, progress)