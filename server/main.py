import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from PIL import Image

load_dotenv()

app = Flask(__name__)
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)

def delete_img(img_path):
    print(img_path)
    os.remove(os.path.relpath(img_path))
        
def find_emotion(img_path): # temp/image_name
    # puts image into neural network to determine emotion
    delete_img(img_path)
    return "EMOTIONAL DAMAGE"


@app.get('/')
def home():
    return "Lol"

@app.get('/api/emotions')
def emotions():
    return find_emotion(img_path="temp/sample1.jpg")

@app.post('/api/image')
def image():
    # upload 
    data = request.get_json()
    image = data["image"]
    return {"type": "SUCCESS", "response": image}

# upload into temp folder then delete from temp folder

if __name__=="__main__":
    app.run(debug=True, port=8080)