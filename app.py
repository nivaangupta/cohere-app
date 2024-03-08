from flask import Flask, render_template, request
import os
from summarize import Summary


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


app = Flask(__name__)
summary = Summary()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/test')
def test():
    filePath = "./uploads/Temperature_actuated_non-touch_automatic_door.pdf"
    return render_template("summary.html", glossary=summary.summarize(filePath))


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        path = os.path.join('uploads', file.filename)
        file.save(path)
        glossary = summary.summarize(path)
        os.remove(path)
        return render_template("summary.html", glossary=glossary)

    else:
        return 'Invalid file format. Please upload a PDF file.'


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == "__main__":
    app.run(debug=True)
