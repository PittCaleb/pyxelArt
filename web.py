import json
from flask import Flask, render_template, request, flash

from utils import allowed_file, get_rendered_filename, get_font_list, get_full_filename, is_image
from pixelart import pyxelart_defaults, get_file_details, PyxelArt

app = Flask(__name__)

DEBUG = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_file():
    if request.method == 'POST':
        form = request.form
        prev_data = json.loads(form['data'].replace("\'", '"'))
        height = int(prev_data['fileDetails']['height'] / (prev_data['fileDetails']['width'] / int(form['width'])))
        if prev_data['fileDetails']['frameRate'] > 0 and int(form['fps']) < prev_data['fileDetails']['frameRate']:
            frame_step = int(prev_data['fileDetails']['frameRate'] / int(form['fps']))
        else:
            frame_step = 1

        pa = PyxelArt(width=request.form['width'], height=height, method=form['method'], show_original=False, show_final=False,
                      file_name=prev_data['filename'], font_name=form['fontSelection'],
                      text_color=form['asciiFontColor'], bg_color=form['asciiBGColor'], frame_step=frame_step)
        pa.convert_file()

        data = {'newFile': pa.new_file_name, 'isImage': is_image(pa.new_file_name),
                'fileExt': pa.new_file_name.rsplit('.', 1)[1]}

        return render_template('results.html', data=data)


@app.route('/settings', methods=['POST'])
def file_selection():
    if request.method == 'POST':
        if 'fileSelection' not in request.files:
            flash('No file to upload')
            return render_template('index.html')

        file = request.files['fileSelection']

        if file.filename == '':
            flash('No selected file')
            return render_template('index.html')

        if file and allowed_file(file.filename):
            file.save(get_full_filename(file.filename))
            data = pyxelart_defaults
            data['filename'] = file.filename
            data['renderedFilename'] = get_rendered_filename(data['filename'], data['method'])
            data['fontList'] = get_font_list()
            data['fileDetails'] = get_file_details(data['filename'])
            data['height'] = int(data['width'] / (data['fileDetails']['width'] / data['fileDetails']['height']))

            return render_template('process.html', data=data)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(port=8000, debug=DEBUG)
