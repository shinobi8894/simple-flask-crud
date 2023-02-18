try:
    # try to import flask, or return error if has not been installed
    from flask import Flask, flash, redirect
    from flask import send_from_directory
except ImportError:
    print("You don't have Flask installed, run `$ pip3 install flask` and try again")
    exit(1)

import os, subprocess
from pymongo import MongoClient
from flask import request
from flask.json import jsonify
from werkzeug.utils import secure_filename
import json
from bson import json_util



# Connecting MongoDB

client = MongoClient('mongodb://localhost:27017/')
mydatabase = client.instagram
mycollection = mydatabase.post


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #disable cache
app.secret_key = '123456789'
app.config['SESSION_TYPE'] = 'filesystem'


UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/load', methods=['POST'])
def load_post():
    posts = mycollection.find()
    convertedData  = list(posts)
    return json.dumps(convertedData,default=json_util.default)

@app.route('/new', methods=['POST'])
def add_new_post():
        if 'postImg' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['postImg']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        caption = request.form['caption']
        mycollection.insert_one({
            "caption":caption,
            "url": app.config['UPLOAD_FOLDER']+"/"+filename
        })
        return "Success"

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    if os.path.exists("app.py"):
        # if app.py exists we use the render function
        out = subprocess.Popen(['python3','app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        return stdout if out.returncode == 0 else f"<pre style='color: red;'>{stdout.decode('utf-8')}</pre>"
    if os.path.exists("index.html"):
        return send_from_directory(static_file_dir, 'index.html')
    else:
        return "<h1 align='center'>404</h1><h2 align='center'>Missing index.html file</h2><p align='center'><img src='https://ucarecdn.com/3a0e7d8b-25f3-4e2f-add2-016064b04075/rigobaby.jpg' /></p>"

# Serving any other image
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

app.run(host='0.0.0.0',port=3000, debug=True, extra_files=['./',])
