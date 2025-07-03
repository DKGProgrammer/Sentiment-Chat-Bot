

from flask import Flask, request, jsonify, send_from_directory
from nlp_utils import detect_emotion
import os, json,uuid

app = Flask(__name__)
conversation_log = []  # Store interactions in memory

last_emotion = None
session_store = {}

@app.route("/")
def serve_home():
    return send_from_directory(os.getcwd(), "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global last_emotion  # we’ll modify this
    user_msg = request.json.get("message", "")
    emotion = detect_emotion(user_msg)

    if last_emotion is None:
        bot_reply = f"I sense you're feeling {emotion}."
    elif last_emotion != emotion:
        bot_reply = f"I sense your mood changed from {last_emotion} to {emotion}."
    else:
        bot_reply = f"You're still feeling {emotion}, I see."

    last_emotion = emotion  # update the stored context

    # Log to memory
    conversation_log.append({
        "user": user_msg,
        "bot": bot_reply,
        "emotion": emotion
    })

    # Log to file
    with open("chat_log.jsonl", "a") as log_file:
        log_file.write(json.dumps({
            "user": user_msg,
            "bot": bot_reply,
            "emotion": emotion
        }) + "\n")

    return jsonify({
        "response": bot_reply,
        "emotion": emotion
    })


if __name__ == "__main__":
    app.run(debug=True)
