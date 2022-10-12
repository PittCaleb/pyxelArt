from flask import Flask, render_template, request, flash

from main import process_file, file_selection

app = Flask(__name__)

DEBUG = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_file_stub():
    if request.method == 'POST':
        data = process_file(request.form)
        return render_template('results.html', data=data)


@app.route('/settings', methods=['POST'])
def file_selection_stub():
    if request.method == 'POST':
        if 'fileSelection' not in request.files:
            flash('No file to upload')
            return render_template('index.html')

        file = request.files['fileSelection']

        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')

        data = file_selection(file)
        return render_template('process.html', data=data)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(port=8000, debug=DEBUG)
