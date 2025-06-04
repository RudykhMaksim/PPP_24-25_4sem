from celery import Celery
from app.core.config import settings
from app.services.huffman import huffman_encode, huffman_decode
from app.services.xor import xor_encrypt, xor_decrypt

app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task
def async_encode(text: str, key: str):
    encoded_data, huffman_codes, padding = huffman_encode(text)
    encrypted_data = xor_encrypt(encoded_data, key)
    return {
        "encoded_data": encrypted_data,
        "key": key,
        "huffman_codes": huffman_codes,
        "padding": padding
    }

@app.task
def async_decode(encoded_data: str, key: str, huffman_codes: dict, padding: int):
    decrypted_data = xor_decrypt(encoded_data, key)
    decoded_text = huffman_decode(decrypted_data, huffman_codes, padding)
    return {"decoded_text": decoded_text}