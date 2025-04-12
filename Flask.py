from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            summary TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    input_text = data.get('text', '')
    summary = generate_summary(input_text)

    # Save to database
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("INSERT INTO summaries (input_text, summary) VALUES (?, ?)", (input_text, summary))
    conn.commit()
    conn.close()

    return jsonify({'summary': summary})

def generate_summary(text):
    sentences = text.split('. ')
    if len(sentences) <= 2:
        return text
    important = sentences[:min(3, len(sentences))]  # simple logic
    return '\n'.join(['• ' + s.strip() for s in important])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
