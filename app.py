import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
import os

from room_logic import create_room, join_room, get_room, save_room
from game_logic import HandCricketGame

# ---------------- Lottie Loaders ----------------
def load_lottie(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_run_anim(run):
    path = f"assets/animations/{run}run.json"
    if os.path.exists(path):
        return load_lottie(path)
    return None

# ---------------- Lottie Assets ----------------
bowl_anim = load_lottie("assets/animations/bowl.json")
out_anim = load_lottie("assets/animations/out.json")
win_anim = load_lottie("assets/animations/win.json")

# ---------------- Streamlit Setup ----------------
st.set_page_config(page_title="MPL Hand Cricket", layout="centered")
st.title("🏏 MPL Hand Cricket - 1v1 Online (No Firebase)")
st.markdown("Create or join a room to play with a friend!")

# 🔁 Auto-refresh every 2 seconds to sync tabs
st.experimental_rerun_interval = 2

# ---------------- Session State Setup ----------------
if "room_id" not in st.session_state:
    st.session_state.room_id = None
    st.session_state.player_role = None
    st.session_state.name = None

# ---------------- Entry Page ----------------
if not st.session_state.room_id:
    tab1, tab2 = st.tabs(["Create Room", "Join Room"])

    with tab1:
        name = st.text_input("Your Name", key="creator_name")
        amount = st.number_input("Entry Amount (₹)", min_value=10, step=10)
        if st.button("Create Room"):
            room_id = create_room(name, amount)
            st.success(f"Room Created! Room ID: `{room_id}`")
            st.session_state.room_id = room_id
            st.session_state.player_role = "player1"
            st.session_state.name = name
            st.rerun()

    with tab2:
        name = st.text_input("Your Name", key="joiner_name")
        join_id = st.text_input("Enter Room ID to Join")
        if st.button("Join Room"):
            success = join_room(join_id, name)
            if success:
                st.success(f"Joined Room `{join_id}`")
                st.session_state.room_id = join_id
                st.session_state.player_role = "player2"
                st.session_state.name = name
                st.rerun()
            else:
                st.error("Failed to join. Room may not exist or is full.")

# ---------------- Game Screen ----------------
else:
    room = get_room(st.session_state.room_id)
    if not room:
        st.error("Room not found.")
        st.session_state.room_id = None
        st.rerun()

    st.subheader(f"Room ID: {room['room_id']}")
    st.markdown(f"**Entry:** ₹{room['entry_amount']} per player")

    p1 = room["players"]["player1"]
    p2 = room["players"]["player2"]

    if not p2["joined"]:
        st.warning("Waiting for Player 2 to join...")
        st.stop()

    my_role = st.session_state.player_role
    opponent = "player2" if my_role == "player1" else "player1"
    my_name = room["players"][my_role]["name"]
    op_name = room["players"][opponent]["name"]

    st.markdown(f"🧍 You are **{my_name}** ({my_role})")
    st.markdown(f"🎯 Playing against **{op_name}**")

    # Show scores
    st.markdown(f"**{p1['name']} (Player 1):** {p1['score']}")
    st.markdown(f"**{p2['name']} (Player 2):** {p2['score']}")

    # Game in progress
    if not room["is_over"]:
        if room["turn"] == my_role:
            st_lottie(bowl_anim, height=200)
            st.markdown("### Your Turn:")
            choice = st.radio("Choose a number", [1, 2, 3, 4, 5, 6], horizontal=True)
            if st.button("Play Turn"):
                bat = choice
                bowl = random.randint(1, 6)
                if bat == bowl:
                    room["is_out"] = True
                    st_lottie(out_anim, height=250, key="out")
                else:
                    room["players"][my_role]["score"] += bat
                    anim = get_run_anim(bat)
                    if anim:
                        st_lottie(anim, height=250, key=f"run{bat}")

                if room["is_out"]:
                    if room["innings"] == 1:
                        room["turn"] = opponent
                        room["is_out"] = False
                        room["innings"] += 1
                    else:
                        room["is_over"] = True
                save_room(st.session_state.room_id, room)
                st.rerun()
        else:
            st.info("Waiting for opponent to play...")

    # Game over
    if room["is_over"]:
        st_lottie(win_anim, height=300)
        s1 = p1["score"]
        s2 = p2["score"]
        winner = None
        if s1 > s2:
            winner = p1["name"]
        elif s2 > s1:
            winner = p2["name"]

        st.header("🏆 Game Over")
        if winner:
            win_amt = round(room["entry_amount"] * 1.9, 2)
            st.success(f"🥇 {winner} wins ₹{win_amt}!")
        else:
            st.info("It's a Draw!")

        if st.button("Leave Room"):
            st.session_state.clear()
