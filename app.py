from flask import Flask, request, jsonify, render_template
import openai
import pandas as pd
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Use .env file or hardcode for testing

# Analyze budget
def analyze_budget(file):
    df = pd.read_csv(file)
    summary = df.groupby('Category')['Amount'].sum()
    insights = ""
    for category, amount in summary.items():
        insights += f"\nYou spent ${amount:.2f} on {category}."
    return insights

# Ask GPT
def ask_ai(question):
    prompt = f"You are a helpful and fun financial literacy assistant. Answer in a simple, engaging way. Question: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use free GPT-3.5
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    answer = ask_ai(question)
    return jsonify({'response': answer})

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    insights = analyze_budget(file)
    return jsonify({'insights': insights})

if __name__ == '__main__':
    app.run(debug=True)
