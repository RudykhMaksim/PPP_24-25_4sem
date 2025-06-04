from collections import Counter
from heapq import heappush, heappop
import base64

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_codes(text: str):
    if not text:
        return {}, ""
    freq = Counter(text)
    heap = []
    for char, f in freq.items():
        heappush(heap, HuffmanNode(char, f))

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        parent = HuffmanNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heappush(heap, parent)

    codes = {}
    def generate_codes(node, code=""):
        if node.char is not None:
            codes[node.char] = code or "0"
        else:
            if node.left:
                generate_codes(node.left, code + "0")
            if node.right:
                generate_codes(node.right, code + "1")
    generate_codes(heap[0])
    return codes

def huffman_encode(text: str):
    codes = build_huffman_codes(text)
    encoded = "".join(codes[char] for char in text)
    padding = (8 - len(encoded) % 8) % 8
    encoded += "0" * padding
    byte_array = bytearray()
    for i in range(0, len(encoded), 8):
        byte = encoded[i:i+8]
        byte_array.append(int(byte, 2))
    return base64.b64encode(byte_array).decode(), codes, padding

def huffman_decode(encoded: str, codes: dict, padding: int):
    encoded_bytes = base64.b64decode(encoded)
    binary = "".join(format(byte, "08b") for byte in encoded_bytes)[:-padding]
    reverse_codes = {v: k for k, v in codes.items()}
    decoded = ""
    current_code = ""
    for bit in binary:
        current_code += bit
        if current_code in reverse_codes:
            decoded += reverse_codes[current_code]
            current_code = ""
    return decoded