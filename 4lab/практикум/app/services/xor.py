def xor_encrypt(text: str, key: str) -> str:
    key = key or "default_key"
    key_bytes = key.encode()
    text_bytes = text.encode()
    result = bytearray()
    for i in range(len(text_bytes)):
        result.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return base64.b64encode(result).decode()

def xor_decrypt(encrypted: str, key: str) -> str:
    key = key or "default_key"
    encrypted_bytes = base64.b64decode(encrypted)
    key_bytes = key.encode()
    result = bytearray()
    for i in range(len(encrypted_bytes)):
        result.append(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)])
    return result.decode()