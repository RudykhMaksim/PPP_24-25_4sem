from fastapi import WebSocket
from app.services.huffman import huffman_encode, huffman_decode
from app.services.xor import xor_encrypt, xor_decrypt
import json

async def handle_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "encode":
                text = data.get("text")
                key = data.get("key")
                encoded_data, huffman_codes, padding = huffman_encode(text)
                encrypted_data = xor_encrypt(encoded_data, key)
                response = {
                    "encoded_data": encrypted_data,
                    "key": key,
                    "huffman_codes": huffman_codes,
                    "padding": padding
                }
                await websocket.send_json(response)
            elif action == "decode":
                encoded_data = data.get("encoded_data")
                key = data.get("key")
                huffman_codes = data.get("huffman_codes")
                padding = data.get("padding")
                decrypted_data = xor_decrypt(encoded_data, key)
                decoded_text = huffman_decode(decrypted_data, huffman_codes, padding)
                response = {"decoded_text": decoded_text}
                await websocket.send_json(response)
            else:
                await websocket.send_json({"error": "Invalid action"})
    except Exception as e:
        await websocket.close()