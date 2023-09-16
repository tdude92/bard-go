import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv( )

app = Flask(__name__)
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

@app.get('/')
def home():
    return "Lol"

@app.get('/api/emotions')
def emotions():
    return "emotions"

@app.post('/api/image')
def image():
    data = request.get_json()
    image = data["image"]
    return {"type": "SUCCESS", "response": image}

if __name__=="__main__":
    app.run(debug=True, port=8080)