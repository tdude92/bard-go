import os
import psycopg2
from PIL import Image
from flask import Flask, flash, redirect, url_for, send_from_directory, jsonify, request

ROOT_FOLDER = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(ROOT_FOLDER, "temp/")
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}
print(ROOT_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def delete_img(img_path):
    print(img_path)
    os.remove(os.path.relpath(img_path))
        
def find_emotion(img_path): # temp/image_name
    # puts image into neural network to determine emotion
    delete_img(img_path)
    return "EMOTIONAL DAMAGE"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def home():
    return "Lol"

@app.get('/api/emotions')
def emotions():
    return find_emotion(img_path="temp/sample1.jpg")

@app.route('/api/image', methods=['GET','POST'])
def upload_file():
    if request.method == "POST":
        # Check if the request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # If the user sent no file, the browser also submits an empty part with no filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/api/image/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__=="__main__":
    app.run(debug=True, port=8080)