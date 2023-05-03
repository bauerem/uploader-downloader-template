from multiprocessing import Process
import time
from flask import Flask, Response, send_file, request, make_response
from flask_cors import CORS
import os
from random import random
from datetime import datetime
from PIL import Image


app = Flask(__name__, static_folder="../build", static_url_path="/")
CORS(app)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static/files"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


def is_allowed_filetype(filename):
    allowed_types = {"pdf", "png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_types


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/api/time", methods=["GET"])
def get_current_time():
    return {"time": time.time()}


def something(input):
    a = 0
    for i in range(100_000_000):
        a = i + 1
    return input


def do_something(init_filename):
    load_path = os.path.join(app.config["UPLOAD_FOLDER"], init_filename)
    input = Image.open(load_path)

    output = something(input)

    # Update file

    out_filename = init_filename.split(".")[0] + "_.png"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], out_filename)
    output.save(save_path)


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["inputFile"]
    extension = file.filename.split(".")[-1]
    token = int(random() * 10**16)

    # Define Server Side Filename
    ss_filename = str(token) + "." + extension

    p = Process(target=do_something, args=[ss_filename])
    p.start()

    if file and is_allowed_filetype(ss_filename):
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], ss_filename))
    else:
        return {"fail": "fail! messed up file(name)"}

    # Make the response body
    response = {
        "status": f"successfully uploaded file to the server. process still alive: {p.is_alive()}",
        "filename": file.filename,
        "token": ss_filename.split(".")[0],
    }
    response = make_response(response)

    # Set Cookies, so that user can later download
    # response.set_cookie('filename', file.filename)
    # response.set_cookie( 'token', ss_filename.split('.')[0], path='/')

    return response


@app.route("/api/stream")
def stream():
    token = request.args.get("token")
    final_filename = token + "_.png"
    final_path = os.path.join(app.config["UPLOAD_FOLDER"], final_filename)

    def get_data():
        while True:
            time.sleep(1)
            if os.path.isfile(final_path):
                yield f"data: done\n\n"
            else:
                yield f"data: not done\n\n"

    return Response(get_data(), mimetype="text/event-stream")


@app.route("/api/download", methods=["POST"])
def download_file():
    data = request.json
    ss_filename = data["token"] + "_.png"

    path = os.path.join(app.config["UPLOAD_FOLDER"], ss_filename)

    if not os.path.isfile(path):
        return make_response("File not found", 404)

    # filename = request.cookies.get("token") + ".png"
    return send_file(path, as_attachment=True)
    # response.set_cookie("filename", "image.png", path="/")
