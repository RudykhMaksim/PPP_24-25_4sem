from fastapi import WebSocket
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast_progress(self, task_id: str, user_id: str, progress: int):
        if user_id in self.active_connections:
            message = {
                "status": "PROGRESS",
                "task_id": task_id,
                "operation": "encode/decode",
                "progress": progress
            }
            for connection in self.active_connections[user_id]:
                await connection.send_text(json.dumps(message))

    async def broadcast_completion(self, task_id: str, user_id: str, result: dict):
        if user_id in self.active_connections:
            message = {
                "status": "COMPLETED",
                "task_id": task_id,
                "operation": "encode/decode",
                "result": result
            }
            for connection in self.active_connections[user_id]:
                await connection.send_text(json.dumps(message))

websocket_manager = WebSocketManager()