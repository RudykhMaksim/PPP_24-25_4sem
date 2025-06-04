from pydantic import BaseModel
from typing import Dict

class EncodeRequest(BaseModel):
    text: str
    key: str

class DecodeRequest(BaseModel):
    encoded_data: str
    key: str
    huffman_codes: Dict[str, str]
    padding: int