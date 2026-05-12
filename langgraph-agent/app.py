from flask import Flask, render_template, request, jsonify
from graph.agent_graph import graph

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    query = request.json.get("query")
    result = graph.invoke({"query": query})
    return jsonify({"response": result["final_answer"]})

if __name__ == "__main__":
    app.run(debug=True)
