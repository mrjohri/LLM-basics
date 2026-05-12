from flask import Flask, render_template, request, jsonify
from chains.search_chain import run_search_chain

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    topic = request.json.get("topic")
    result = run_search_chain(topic)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)