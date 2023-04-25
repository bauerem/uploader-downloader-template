from multiprocessing import Process
import time
from flask import Flask, Response, send_file, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from random import random
from datetime import datetime

app = Flask(__name__, static_folder="../build", static_url_path='/')
CORS(app)
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

def do_something(a):
    for i in range(100_000):
        a = i + 1

@app.route('/api/upload', methods=['POST'])
def upload():

    p = Process(target=do_something, args=[1])
    p.start()
    print(p.is_alive())

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
    print(p.is_alive())
    response = {"status": f"successfully uploaded file to the server. process status: {p.is_alive()}", "filename": file.filename}
    response = make_response(response)
    ## response = render_template('index.html')

    # Set Cookies, so that user can later download
    #response.set_cookie('filename', file.filename)
    response.set_cookie('token', ss_filename)
    return response

@app.route('/api/stream')
def stream():
    token = request.args.get('token')
    def get_data():
        while True:
            time.sleep(1)
            print(token)
            yield f'data: {datetime.now()} \n\n'

    return Response(get_data(), mimetype='text/event-stream')

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
    response.headers["Content-Disposition"] = "attachment; filename={}".format(ss_filename)
    #response.headers.set('Content-Disposition', 'attachment', filename=ss_filename)
    return response