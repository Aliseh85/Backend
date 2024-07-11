from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('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')

# Database configuration from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aliseh:aliseh@localhost:5432/insait_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    answer = db.Column(db.String)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question_text = data.get('question')

    if not question_text:
        return jsonify({'error': 'No question provided'}), 400

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question_text,
            max_tokens=150
        )
        answer_text = response.choices[0].text.strip()

        # Save question and answer to the database
        question = Question(text=question_text, answer=answer_text)
        db.session.add(question)
        db.session.commit()

        return jsonify({'answer': answer_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
