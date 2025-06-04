import asyncio
import websockets
import json
import uuid
import argparse
import aiohttp

async def authenticate():
    email = input("Enter email: ")
    password = input("Enter password: ")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/auth/login/",
            json={"email": email, "password": password}
        ) as response:
            if response.status != 200:
                raise Exception(f"Authentication failed: {await response.text()}")
            data = await response.json()
            return data.get("access_token"), email

async def websocket_client(token: str, user_id: str, task_id: str):
    headers = {"Authorization": f"Bearer {token}"}
    uri = f"ws://localhost:8000/encode/ws/{user_id}"
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Notification: {message}")

async def send_task(token: str, user_id: str, action: str, data: dict):
    task_id = str(uuid.uuid4())
    data["task_id"] = task_id
    data["action"] = action
    headers = {"Authorization": f"Bearer {token}"}
    uri = f"ws://localhost:8000/encode/ws/{user_id}"
    async with websockets.connect(uri, extra_headers=headers) as websocket:
        await websocket.send(json.dumps(data))
        asyncio.create_task(websocket_client(token, user_id, task_id))

async def main():
    parser = argparse.ArgumentParser(description="Console client for Encryption API")
    parser.add_argument("--file", type=str, help="Path to script file")
    args = parser.parse_args()

    token, email = await authenticate()
    user_id = input("Enter user ID (should match your email): ")
    if user_id != email:
        print(f"Error: user_id ({user_id}) must match your email ({email})")
        return

    if args.file:
        with open(args.file, "r") as f:
            for line in f:
                command = json.loads(line.strip())
                await send_task(token, user_id, command.get("action"), command)
    else:
        while True:
            command = input("Enter command (encode/decode) or 'quit' to exit: ")
            if command == "quit":
                break
            if command in ["encode", "decode"]:
                data = {}
                if command == "encode":
                    data["text"] = input("Enter text to encode: ")
                    data["key"] = input("Enter key: ")
                else:
                    data["encoded_data"] = input("Enter encoded data: ")
                    data["key"] = input("Enter key: ")
                    data["huffman_codes"] = json.loads(input("Enter huffman codes (JSON): "))
                    data["padding"] = int(input("Enter padding: "))
                await send_task(token, user_id, command, data)

if __name__ == "__main__":
    asyncio.run(main())