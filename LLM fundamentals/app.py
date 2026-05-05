from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"


def generate_response(messages, temperature=0.7, max_tokens=200, top_p=1):
    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return chat_completion.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    user_message = data.get("message", "")
    panels = data.get("panels", [])

    responses = []

    for panel in panels:
        history = panel.get("history", [])

        # Add user message
        history.append({"role": "user", "content": user_message})

        # ✅ SAFE parameter extraction
        temperature = panel.get("temperature", 0.7)
        max_tokens = panel.get("max_tokens", 200)
        top_p = panel.get("top_p", 1)

        response = generate_response(
            messages=history,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p
        )

        history.append({"role": "assistant", "content": response})

        responses.append({
            "response": response,
            "history": history
        })

    return jsonify(responses)


if __name__ == "__main__":
    app.run(debug=True)