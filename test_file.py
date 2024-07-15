import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Question

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ali@localhost:5432/insait_database_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_ask(client, mocker):
    mock_response = {
        'choices': [{'text': 'This is a test answer'}]
    }
    mocker.patch('openai.Completion.create', return_value=mock_response)

    response = client.post('/ask', json={'question': 'What is the capital of France?'})
    assert response.status_code == 200
    assert response.json == {'answer': 'This is a test answer'}

    # Check if the question was saved in the database
    question = Question.query.first()
    assert question.text == 'What is the capital of France?'
    assert question.answer == 'This is a test answer'

def test_ask_no_question(client):
    response = client.post('/ask', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'No question provided'}

def test_ask_openai_error(client, mocker):
    mocker.patch('openai.Completion.create', side_effect=Exception('OpenAI error'))

    response = client.post('/ask', json={'question': 'What is the capital of France?'})
    assert response.status_code == 500
    assert response.json == {'error': 'OpenAI error'}
