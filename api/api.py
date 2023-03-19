import time
from flask import Flask, Response, send_file, render_template, request, make_response
from werkzeug.utils import secure_filename
import os
from random import random

app = Flask(__name__, static_folder="../build", static_url_path='/')
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'static/files'
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def is_allowed_filetype(filename):
    allowed_types = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_types

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/time', methods=['GET'])
def get_current_time():
    return {'time': time.time()}

@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    extension = file.filename.split('.')[-1]
    token = int(random()*10**16)

    # Define Server Side Filename
    ss_filename = str(token) + '.' + extension 
    if file and is_allowed_filetype( ss_filename ):
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'],
            ss_filename
        ))
    else:
        return {"fail": "fail! messed up file(name)"}
    

    # Make the response body
    response = {"status": "successfully uplaoded file to the server.", "filename": file.filename}
    response = make_response(response)
    ## response = render_template('index.html')

    # Set Cookies, so that user can later download
    #response.set_cookie('filename', file.filename)
    response.set_cookie('token', ss_filename)
    return response

@app.route('/api/download')
def download_file():
    ss_filename = request.cookies.get('token')
    path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        ss_filename
    )

    if not os.path.exists(path):
        return make_response("File not found", 404)
    
    response = make_response(send_file(path, as_attachment=True))
    #response.headers["Content-Disposition"] = "attachment; filename={}".format(request.cookies.get('filename'))
    response.headers.set('Content-Disposition', 'attachment', filename=ss_filename)
    return response