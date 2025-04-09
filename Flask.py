from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Connects Flask to your HTML

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    summary = simple_summarize(text)
    return jsonify({"summary": summary})

def simple_summarize(text):
    sentences = text.split('. ')
    if len(sentences) <= 2:
        return text
    important = sentences[:max(1, len(sentences)//3)]
    return '. '.join(important).strip() + '.'

if __name__ == "__main__":
    app.run(debug=True)
