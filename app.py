from flask import Flask, request, jsonify, render_template
from agent.agent import ai_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = ai_agent(user_message)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
