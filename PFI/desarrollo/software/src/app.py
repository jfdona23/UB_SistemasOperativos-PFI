"""
Application to show the IRQ workflow and other useful things.
"""
import os
from flask import Flask, render_template, abort, request, redirect
from flask.helpers import make_response

from logic import IRQAppLogic


# App config zone
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB max upload
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.txt']
app.config['UPLOAD_PATH'] = 'assets'

# Create Logic object
logic = IRQAppLogic(app.config['UPLOAD_PATH'])

# Routing zone
@app.route('/', methods=['GET'])
def home():
    """
    Main page, a.k.a. landing page.
    Workflow result is shown here.
    """
    irqData = logic.processAll()
    return render_template("index.html", irqData=irqData)

@app.route('/', methods=['POST'])
def uploadFile():
    """
    Uploads a file to be processed and stores it in UPLOAD_FOLDER
    """
    # uploaded_file = request.files['file']             # Single File
    for uploaded_file in request.files.getlist('file'): # Multi files
        if uploaded_file.filename != '':
            fileExtension = os.path.splitext(uploaded_file.filename)[1]
            if fileExtension not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            fileToUpload = os.path.join(app.config['UPLOAD_PATH'],
                           str(abs(hash(uploaded_file.filename))) +
                           fileExtension)
            uploaded_file.save(fileToUpload)
        else:
            redirect(request.url)
    return redirect(request.url)

@app.route('/irq', methods=['GET'])
def currentIRQ():
    """
    Show several counters for the IRQ running in the server
    """
    return render_template("myirq.html", output=logic.showInterruptStats())

@app.route('/plain', methods=['GET'])
def plain():
    """
    Plain response with the IRQ counters used by currentIRQ() method.
    This endpoint is only accessible by redirection.
    """
    if 'Referer' not in request.headers.keys():
        abort(403)
    response = make_response(logic.showInterruptStats())
    response.headers["content-type"] = "text/plain"
    return response

@app.route('/ping', methods=['GET'])
def healthz():
    """
    Health check. It should respond "pong".
    """
    return 'pong'


if __name__ == "__main__":
    app.run(host="0.0.0.0")