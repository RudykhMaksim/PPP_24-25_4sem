from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from app.schemas.encode import EncodeRequest, DecodeRequest
from app.celery.tasks import async_encode, async_decode
from app.core.security import decode_token, get_current_user
from app.websocket.websocket_manager import websocket_manager
import json
import uuid

router = APIRouter()

async def get_websocket_user(websocket: WebSocket):
    # Извлекаем заголовок Authorization
    auth_header = websocket.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Bearer token required")
    token = auth_header[len("Bearer "):]
    try:
        payload = decode_token(token)
        return {"email": payload.get("sub")}
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")

@router.websocket("/encode/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    current_user = await get_websocket_user(websocket)
    if user_id != current_user["email"]:
        await websocket.accept()
        await websocket.send_text(json.dumps({"error": "Invalid user_id"}))
        await websocket.close(code=1008)  # Policy Violation
        raise HTTPException(status_code=403, detail="Invalid user_id")
    await websocket_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            task_id = request.get("task_id")
            if request.get("action") == "encode":
                task = async_encode.delay(request["text"], request["key"], task_id, user_id)
            elif request.get("action") == "decode":
                task = async_decode.delay(
                    request["encoded_data"],
                    request["key"],
                    request["huffman_codes"],
                    request["padding"],
                    task_id,
                    user_id
                )
    except WebSocketDisconnect:
        websocket_manager.disconnect(task_id)

@router.post("/encode/encode", response_model=dict)
async def encode(data: EncodeRequest, current_user: dict = Depends(get_current_user)):
    task = async_encode.delay(data.text, data.key, str(uuid.uuid4()), current_user["email"])
    return {"task_id": task.id, "status": "STARTED"}

@router.post("/encode/decode", response_model=dict)
async def decode(data: DecodeRequest, current_user: dict = Depends(get_current_user)):
    task = async_decode.delay(
        data.encoded_data,
        data.key,
        data.huffman_codes,
        data.padding,
        str(uuid.uuid4()),
        current_user["email"]
    )
    return {"task_id": task.id, "status": "STARTED"}