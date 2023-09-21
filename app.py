import os
import uuid
from custom_errors import *
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

logs_list = []
allowed_file_types = ['application/pdf']

os.makedirs(os.path.join(app.instance_path, "uploads"), exist_ok=True)


def log(msg: str):
    logs_list.append(msg)


def rename_uploaded_filename(filename: str):
    filename = f"{uuid.uuid4()}-{secure_filename(filename)}"
    log(filename)
    return filename


def get_uploaded_file_path(filename):
    return os.path.join(app.instance_path, "uploads", filename)


def save_file(uploaded_file, filename):
    file_path: str = get_uploaded_file_path(filename)
    log(file_path)
    uploaded_file.save(file_path)
    log("file saved")


def get_uploaded_file_details(uploaded_file):
    details = {
        "content_type": uploaded_file.content_type,
        "filename": uploaded_file.filename,
        "mimetype": uploaded_file.mimetype,
    }
    return details


def get_uploaded_file(request):
    return request.files["file"]


def remove_saved_file(filename):
    file_path = get_uploaded_file_path(filename)
    os.remove(file_path)
    log("File removed")


def validate_uploaded_file(uploaded_file):
    if uploaded_file.filename == "":
        raise NoFileUploadedError()


@app.route('/', methods=['GET', 'POST'])
def index():
    log("I loaded")
    if request.method == 'POST':
        if "file" in request.files:
            log("file found")

        uploaded_file = get_uploaded_file(request)
        try:
            validate_uploaded_file(uploaded_file)
        except NoFileUploadedError as e:
            flash(e.message)

        uploaded_file_details = get_uploaded_file_details(uploaded_file)
        uploaded_file_type: str = uploaded_file_details["content_type"]
        filename: str = rename_uploaded_filename(uploaded_file_details["filename"])
        save_file(uploaded_file, filename)

        if uploaded_file_type in allowed_file_types:
            log("file allowed")

        log("file vectorized")

        remove_saved_file(filename)

    elif request.method == 'GET':
        log("method get")
        
    log_copy = logs_list.copy()
    logs_list.clear()
    
    return render_template('index.html', logs=log_copy, method=request.method)

