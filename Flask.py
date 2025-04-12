from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import math

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
    compression = int(data.get('compression', 30))  # Value from slider

    summary = generate_summary(input_text, compression)

    # Save to database
    conn = sqlite3.connect('summarizer.db')
    c = conn.cursor()
    c.execute("INSERT INTO summaries (input_text, summary) VALUES (?, ?)", (input_text, summary))
    conn.commit()
    conn.close()

    return jsonify({'summary': summary})


def generate_summary(text, compression):
    sentences = text.split('. ')
    total_sentences = len(sentences)

    if total_sentences <= 2:
        return text

    # Invert compression logic: higher % = shorter summary
    keep_ratio = (100 - compression) / 100
    keep_count = max(1, math.ceil(keep_ratio * total_sentences))

    # Select first N sentences
    selected = sentences[:keep_count]

    return '\n'.join(['• ' + s.strip() for s in selected if s.strip()])


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
