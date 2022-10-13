import json
from time import time

from src.pyxelart import pyxelart_defaults, get_file_details, PyxelArt
from src.utils import allowed_file, get_rendered_filename, get_font_list, get_full_filename, is_image, purge_temp_dir


def process_file(form):
    prev_data = json.loads(form['data'].replace("\'", '"'))
    height = int(prev_data['fileDetails']['height'] / (prev_data['fileDetails']['width'] / int(form['width'])))
    if prev_data['fileDetails']['frameRate'] > 0 and int(form['fps']) < prev_data['fileDetails']['frameRate']:
        frame_step = round(prev_data['fileDetails']['frameRate'] / int(form['fps']))
    else:
        frame_step = 1

    if not prev_data['isImage'] and form['button'] == 'preview':
        file_name = form['imageDisplayed'] if '/' not in form['imageDisplayed'] else \
            form['imageDisplayed'].rsplit('/', 1)[1]
    else:
        file_name = prev_data['filename']

    ascii_char_set = 'complex' if 'asciiCharSet' in form else 'simple'

    pa = PyxelArt(width=form['width'], height=height, method=form['method'], show_original=False, show_final=False,
                  file_name=file_name, font_name=form['fontSelection'], text_color=form['asciiFontColor'],
                  bg_color=form['asciiBGColor'], frame_step=frame_step, ascii_char_set=ascii_char_set)
    t1 = time()
    pa.convert_file()
    t2 = time()

    tpf = prev_data['timePerFrame'] if 'mp4' in pa.new_file_name else (t2-t1)
    est = tpf * prev_data['fileDetails']['frames'] * int(form['fps']) / prev_data['fileDetails']['frameRate'] / 60

    show_image = prev_data['showImage'] if 'mp4' in pa.new_file_name else pa.new_file_name
    show_image = show_image.rsplit('/', 1)[1] if '/' in show_image else show_image

    video_file = pa.new_file_name if 'mp4' in pa.new_file_name else ''

    data = prev_data
    data.update({
        'showImage': show_image,
        'videoFile': video_file,
        'width': form['width'],
        'method': form['method'],
        'textColor': form['asciiFontColor'],
        'asciiBackground': form['asciiBGColor'],
        'asciiFont': form['fontSelection'],
        'displayImage': form['imageDisplayed'],
        'fps': form['fps'],
        'origFPS': prev_data['fileDetails']['frameRate'],
        'timePerFrame': tpf,
        'initialEncodingEst': round(est, 1),
        'asciiCharSet': ascii_char_set
    })

    return data


def file_selection(file):
    if file and allowed_file(file.filename):
        purge_temp_dir()
        file.save(get_full_filename(file.filename))
        details = get_file_details(file.filename)
        is_file_image = is_image(file.filename)
        data = pyxelart_defaults

        if is_file_image:
            show_image = file.filename
        else:
            show_image = details['thumbnails'][2]

        data.update({
            'filename': file.filename,
            'showImage': show_image,
            'renderedFilename': get_rendered_filename(file.filename, data['method']),
            'fontList': get_font_list(),
            'fileDetails': details,
            'height': int(data['width'] / (details['width'] / details['height'])),
            'isImage': 1 if is_file_image else 0,
            'displayImage': show_image,
            'timePerFrame': details['timePerFrame'],
            'initialEncodingEst': details['initialEncodingEst'],
            'fps': details['frameRate'],
            'origFPS': details['frameRate']
        })

        return data
