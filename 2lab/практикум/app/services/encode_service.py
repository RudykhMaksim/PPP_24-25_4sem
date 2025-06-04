import base64
import hmac
import hashlib
from collections import defaultdict

def build_huffman_tree(text: str) -> tuple:
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    # Построение дерева Хаффмана
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    while len(heap) > 1:
        lo = min(heap, key=lambda x: x[0])
        heap.remove(lo)
        hi = min(heap, key=lambda x: x[0])
        heap.remove(hi)
        for pair in lo[1:]:
            pair[1] = "0" + pair[1]
        for pair in hi[1:]:
            pair[1] = "1" + pair[1]
        heap.append([lo[0] + hi[0]] + lo[1:] + hi[1:])

    huffman_codes = dict(heap[0][1:]) if heap else {}
    return huffman_codes

def huffman_encode(text: str, huffman_codes: dict) -> tuple[str, int]:
    encoded = "".join(huffman_codes[char] for char in text)
    padding = (8 - len(encoded) % 8) % 8
    encoded += "0" * padding
    byte_array = bytearray()
    for i in range(0, len(encoded), 8):
        byte = encoded[i:i + 8]
        byte_array.append(int(byte, 2))
    return base64.b64encode(byte_array).decode('utf-8'), padding

def encrypt_with_key(data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    data_bytes = data.encode('utf-8')
    hmac_obj = hmac.new(key_bytes, data_bytes, hashlib.sha256)
    encrypted = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return encrypted

def encode_text(text: str, key: str) -> dict:
    huffman_codes = build_huffman_tree(text)
    encoded, padding = huffman_encode(text, huffman_codes)
    encrypted = encrypt_with_key(encoded, key)
    return {
        "encoded_data": encrypted,
        "huffman_codes": huffman_codes,
        "padding": padding
    }

def huffman_decode(encoded_data: str, huffman_codes: dict, padding: int) -> str:
    decoded_bits = ""
    byte_array = base64.b64decode(encoded_data.encode('utf-8'))
    for byte in byte_array:
        bits = bin(byte)[2:].zfill(8)
        decoded_bits += bits
    decoded_bits = decoded_bits[:-padding] if padding else decoded_bits

    reverse_codes = {code: char for char, code in huffman_codes.items()}
    current_code = ""
    decoded_text = ""
    for bit in decoded_bits:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""
    return decoded_text

def decrypt_with_key(encrypted_data: str, key: str) -> str:
    key_bytes = key.encode('utf-8')
    expected_hmac = base64.b64decode(encrypted_data.encode('utf-8'))
    return base64.b64encode(expected_hmac).decode('utf-8')

def decode_text(encoded_data: str, key: str, huffman_codes: dict, padding: int) -> str:
    decrypted = decrypt_with_key(encoded_data, key)
    decoded = huffman_decode(decrypted, huffman_codes, padding)
    return decoded