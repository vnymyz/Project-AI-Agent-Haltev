from flask import Flask, request, jsonify, render_template
from agent.agent import handle_message

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

    try:
        response = handle_message(user_message)
    except Exception as e:
        # fallback aman
        response = "Terjadi kesalahan saat memproses permintaan."

    return jsonify({
        "user_input": user_message,
        "response": response
    })

if __name__ == "__main__":
    app.run(debug=True)
