import os
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import rag

load_dotenv(override=True)

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(path)
    rag.build_index(path)
    return jsonify({"message": f"'{file.filename}' indexed successfully."})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400

    context_chunks = rag.retrieve(query)
    context = "\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Answer the user's question using only "
                "the provided context. If the answer is not in the context, say so.\n\n"
                f"Context:\n{context}"
            ),
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    return jsonify({"answer": response.choices[0].message.content})


if __name__ == "__main__":
    app.run(debug=True)
