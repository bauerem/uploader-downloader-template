from multiprocessing import Process
import time
from flask import Flask, Response, send_file, request, make_response
from flask_cors import CORS
import os
from random import random
from datetime import datetime
from PIL import Image
import magic

app = Flask(__name__, static_folder="../build", static_url_path="/")
CORS(app)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static/files"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

OUTPUT_EXTENSION = ".png"


def is_allowed_filetype():
    # Define allowed mime types
    allowed_mime_types = ["image/png", "image/jpeg", "text/plain", "application/pdf"]

    # Read the first 2048 bytes from the uploaded file buffer. We don't save it to the
    # filesystem yet because we don't know wtf it could be.
    mime = magic.Magic(mime=True)
    file = request.files["inputFile"]
    first_2kb = file.read(2048)
    detected_mimetype = mime.from_buffer(first_2kb)

    # Reset stream to start of file
    file.stream.seek(0)

    print("\n\n Uploaded mimetype: ", detected_mimetype, "\n\n")

    # Check mimetype
    if detected_mimetype in allowed_mime_types:
        return True

    return False

    # return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_types


def get_filename(token, suffix=None):
    # Get names of all files in the upload folder
    filenames = os.listdir(app.config["UPLOAD_FOLDER"])

    # Look for the correct filename that contains the token.
    # Note: "filename" is always unique since we check for uniqueness when we
    # store it.
    filename = list(filter(lambda filename: token in filename, filenames))[0]

    extension = filename.split(".")[-1]

    # Get the currently processed file
    if suffix is not None:
        final_filename = token + suffix + "." + extension
    else:
        final_filename = token + "." + extension

    return final_filename


@app.route("/")
def index():
    return "The API works."


@app.route("/api/time", methods=["GET"])
def get_current_time():
    return {"time": time.time()}


def something(input):
    a = 0
    for i in range(100_000_000):
        a = i + 1
    return input


def do_something(init_filename):
    # Load file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], init_filename)
    input = Image.open(filepath)

    # Here we'd change the file somehow. We just wait 3 seconds.
    time.sleep(3)

    # Update file: We set the input as the output (because we didn't do
    # anything) and save it undera new name.
    output = input
    extension = input.filename.split(".")[-1]
    out_filename = init_filename.split(".")[0] + "_." + extension
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], out_filename)
    output.save(save_path)


@app.route("/api/upload", methods=["POST"])
def upload():
    # Check if the file contained in the request's body is allowed.
    if not is_allowed_filetype():
        return "Unsupported filetype", 415

    # Generate token
    file = request.files["inputFile"]
    extension = file.filename.split(".")[-1]
    token = int(random() * 10**16)

    # Define Server side filename
    ss_filename = str(token) + "." + extension

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], ss_filename)

    # Store file to filesystem
    if os.path.isfile(filepath):
        # TODO: Maybe just generate a new token?
        return "File with this token already exists.", 409

    file.save(filepath)

    # Start service that does something with file.
    print(os.path.join(app.config["UPLOAD_FOLDER"], ss_filename))
    p = Process(target=do_something, args=[ss_filename])
    p.start()

    # Make the response body
    response = {
        "status": f"successfully uploaded file to the server. process still alive: {p.is_alive()}",
        "filename": file.filename,
        "token": ss_filename.split(".")[0],
    }

    return response


@app.route("/api/stream")
def stream():
    token = request.args.get("token")

    final_filename = get_filename(token, suffix="_")

    final_path = os.path.join(app.config["UPLOAD_FOLDER"], final_filename)

    # Wait until the file is processed
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
    # Get token
    data = request.json
    token = data["token"]

    # Get filename
    ss_filename = get_filename(token, suffix="_")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], ss_filename)

    # Check if file exists
    if not os.path.isfile(filepath):
        return make_response("File not found", 404)

    # Send file back to client
    return send_file(filepath, as_attachment=True)
