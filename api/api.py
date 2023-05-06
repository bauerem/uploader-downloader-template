from multiprocessing import Process
import time
from flask import Flask, Response, send_file, request, make_response, session
from flask_cors import CORS
import os
from random import random
from datetime import datetime
from PIL import Image
import magic

from service import Service

# TODO: Use secure_filename()
# TODO: Use sessions
# TODO: Utilize UPLOAD_FOLDER and MAX_CONTENT_LENGTH and TEMP DIR

app = Flask(__name__, static_folder="../build", static_url_path="/")
CORS(app)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "static/files"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/")
def index():
    return "The API works."


@app.route("/api/time", methods=["GET"])
def get_current_time():
    return {"time": time.time()}


@app.route("/api/upload", methods=["POST"])
def upload():
    # Generate token
    token = str(int(random() * 10**16))

    # Get file extension
    file = request.files["inputFile"]
    input_extension = file.filename.split(".")[-1]

    service = Service(token, input_extension)

    # Check if the file contained in the request's body is allowed.
    if not is_allowed_filetype(service.allowed_mime_types):
        return "Unsupported filetype", 415

    # Store file to filesystem
    if os.path.isfile(service.path_input_file):
        # TODO: Maybe just generate a new token?
        return "File with this token already exists.", 409

    file.save(service.path_input_file)

    # Start service that does something with file.
    p = Process(target=service.process)
    p.start()

    # Make the response body
    response = {
        "status": f"successfully uploaded file to the server. process still alive: {p.is_alive()}",
        "filename": file.filename,
        "token": token,
    }

    return response


@app.route("/api/stream")
def stream():
    token = request.args.get("token")

    service = Service(token)

    # Wait until the file is processed
    def get_data():
        while True:
            time.sleep(1)
            if os.path.isfile(service.path_processed_file):
                yield f"data: done\n\n"
            else:
                yield f"data: not done\n\n"

    return Response(get_data(), mimetype="text/event-stream")


@app.route("/api/download", methods=["POST"])
def download_file():
    # Get token
    data = request.json
    token = data["token"]

    service = Service(token)

    # Check if file exists
    if not os.path.isfile(service.path_processed_file):
        return make_response("File not found", 404)

    # Send file back to client
    return send_file(service.path_processed_file, as_attachment=True)


def is_allowed_filetype(allowed_mime_types):
    # Read the first 2048 bytes from the uploaded file buffer. We don't save it to the
    # filesystem yet because we don't know wtf it could be.
    mime = magic.Magic(mime=True)
    file = request.files["inputFile"]
    first_2kb = file.read(2048)
    detected_mimetype = mime.from_buffer(first_2kb)

    # Reset stream to start of file
    file.stream.seek(0)

    # Check mimetype
    if detected_mimetype in allowed_mime_types:
        return True

    return False
