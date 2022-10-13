import os
import glob
from time import time

IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
VIDEO_EXTENSIONS = ['mp4', 'avi']
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS

RENDERED_IMAGE_EXTENSION = 'png'
RENDERED_VIDEO_EXTENSION = 'mp4'

FONT_DIRECTORY = 'fonts'
FONT_TYPE = 'ttf'

TMP_DIR = 'static/tmp'


def timer_func(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


def get_full_filename(filename):
    return os.path.join(os.getcwd(), TMP_DIR, filename)


def convert_to_gray(rgb):
    return int(0.2989 * rgb[0] + 0.5870 * rgb[1] + 0.1140 * rgb[2])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_image(filename):
    return filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS


def get_rendered_filename(filenameext, method):
    filename, ext = filenameext.rsplit('.', 1)
    rendered_extension = RENDERED_VIDEO_EXTENSION if ext in VIDEO_EXTENSIONS else RENDERED_IMAGE_EXTENSION
    return f'{filename}-{method}.{rendered_extension}'


def get_font_list():
    dir_list = os.listdir(FONT_DIRECTORY)
    fonts_available = []
    for file in dir_list:
        if FONT_TYPE in file:
            fonts_available.append(file.rsplit('.', 1)[0])
    return fonts_available


def purge_temp_dir():
    files = glob.glob(os.path.join(os.getcwd(), TMP_DIR, '*'))

    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            print(f'Unable to remove file {e}')
