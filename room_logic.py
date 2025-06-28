import os
import json
import random

ROOM_DIR = "rooms"

def ensure_dir():
    if not os.path.exists(ROOM_DIR):
        os.makedirs(ROOM_DIR)

def generate_room_id():
    return str(random.randint(100000, 999999))

def create_room(player_name, entry_amount):
    ensure_dir()
    room_id = generate_room_id()
    data = {
        "room_id": room_id,
        "entry_amount": entry_amount,
        "players": {
            "player1": {"name": player_name, "joined": True, "score": 0},
            "player2": {"name": "", "joined": False, "score": 0}
        },
        "turn": "player1",
        "innings": 1,
        "is_out": False,
        "is_over": False
    }
    save_room(room_id, data)
    return room_id

def join_room(room_id, player_name):
    path = os.path.join(ROOM_DIR, f"{room_id}.json")
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if data["players"]["player2"]["joined"]:
        return False
    data["players"]["player2"] = {"name": player_name, "joined": True, "score": 0}
    save_room(room_id, data)
    return True

def get_room(room_id):
    try:
        with open(os.path.join(ROOM_DIR, f"{room_id}.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save_room(room_id, data):
    with open(os.path.join(ROOM_DIR, f"{room_id}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
