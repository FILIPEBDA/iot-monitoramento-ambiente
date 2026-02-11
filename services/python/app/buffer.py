import json
import os
import time

BUFFER_FILE = "/app/buffer.jsonl"

def save_to_buffer(dados):
    with open(BUFFER_FILE, "a") as f:
        f.write(json.dumps(dados) + "\n")

def load_buffer():
    if not os.path.exists(BUFFER_FILE):
        return []

    with open(BUFFER_FILE, "r") as f:
        lines = f.readlines()

    return [json.loads(l) for l in lines]

def clear_buffer():
    if os.path.exists(BUFFER_FILE):
        os.remove(BUFFER_FILE)
