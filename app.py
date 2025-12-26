from flask import Flask, request, jsonify, render_template
from agent.agent import ai_agent
from agent.nlp import detect_intent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"response": "Pesan tidak boleh kosong"}), 400

    user_message = data.get("message", "").strip()
    if user_message == "":
        return jsonify({"response": "Silakan masukkan pertanyaan"}), 400

    # 🔹 DEBUG: cek intent
    intent = detect_intent(user_message)

    # 🔹 MAIN AI RESPONSE
    response = ai_agent(user_message)

    return jsonify({
        "user_input": user_message,
        "detected_intent": intent,   # <-- penting buat testing
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)
