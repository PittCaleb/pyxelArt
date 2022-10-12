import cv2
import numpy

from PIL import Image, ImageDraw, ImageFont, ImageColor

from utils import timer_func, convert_to_gray, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS, get_full_filename, \
    get_rendered_filename

pyxelart_defaults = {
    'width': 128,
    'height': 72,
    'method': 'pyxelate',
    'font_size': 20,
    'asciiFont': 'Decoder',
    'textColor': '#18F212',
    'asciiBackground': '#000000',
    'frame_step': 4,
}

ASCII_TABLE_SIMPLE = " .:-=+*#%@"
ASCII_TABLE_DETAILED = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_file_details(filename):
    filename = get_full_filename(filename)
    if filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS:
        image = Image.open(filename)
        file_details = {'frameRate': 0,
                        'width': image.width,
                        'height': image.height}
    else:
        video = cv2.VideoCapture(filename)  # says we capture an image from a webcam
        file_details = {'frameRate': int(video.get(5)),
                        'width': int(video.get(3)),
                        'height': int(video.get(4))}
        video.release()
    return file_details


class PyxelArt:
    def __init__(self, width=128, height=72, method='pyxelate', show_original=False, file_name='', font_name='Decoder',
                 text_color='#18F212', bg_color='#000000', frame_step=4, show_final=True):
        self.width = int(width)
        self.height = int(height)
        self.method = method
        self.show_original = show_original
        self.show_final = show_final
        self.file_name = file_name

        self.new_file_name = get_rendered_filename(self.file_name, self.method)

        self.ascii_table = ASCII_TABLE_DETAILED
        self.ascii_chunks = 256 / len(self.ascii_table)

        self.font_size = 20  # ToDo: Need to change based on chunk size, 20 works in my image test
        self.ascii_font = ImageFont.truetype(f'fonts/{font_name}.ttf', self.font_size)
        self.text_color = ImageColor.getcolor(text_color, "RGB")
        self.ascii_background = ImageColor.getcolor(bg_color, "RGB")

        self.frame_step = frame_step

        self.image = None
        self.pixels = None
        self.draw = None
        self.new_image = None
        self.new_draw = None

    # @timer_func
    def chunk_image(self, console_ascii=False):
        x_ratio = self.image.width / self.width
        y_ratio = self.image.height / self.height

        for y in range(0, self.height):
            for x in range(0, self.width):
                pixel_count = 0
                pixel_sum = (0, 0, 0)
                for y_sub in range(int(y * y_ratio), int((y + 1) * y_ratio)):
                    for x_sub in range(int(x * x_ratio), int((x + 1) * x_ratio)):
                        pt = self.pixels[x_sub, y_sub]
                        pixel_sum = (pixel_sum[0] + pt[0], pixel_sum[1] + pt[1], pixel_sum[2] + pt[2])
                        pixel_count += 1

                # Pyxelate default
                pixel_avg = (
                    int(pixel_sum[0] / pixel_count), int(pixel_sum[1] / pixel_count),
                    int(pixel_sum[2] / pixel_count))

                if self.method in ('greyscale', 'ascii'):
                    grey = convert_to_gray(pixel_avg)

                    if self.method == 'greyscale':
                        pixel_avg = (grey, grey, grey)

                    if self.method == 'ascii':
                        grey_char = self.ascii_table[int(grey / self.ascii_chunks)]
                        if console_ascii:
                            print(grey_char, end='')

                        self.new_draw.text((int(x * x_ratio), int(y * y_ratio)), grey_char, fill=self.text_color,
                                           font=self.ascii_font)

                # Update the image for pyxelate and greyscale
                if self.method != 'ascii':
                    for x_sub in range(int(x * x_ratio), int((x + 1) * x_ratio)):
                        for y_sub in range(int(y * y_ratio), int((y + 1) * y_ratio)):
                            self.pixels[x_sub, y_sub] = pixel_avg

            if console_ascii:
                print('')

        if self.method == 'ascii':
            self.image = self.new_image

    def open_image(self):
        try:
            self.image = Image.open(get_full_filename(self.file_name))
            self.pixels = self.image.load()
            self.draw = ImageDraw.Draw(self.image)

            self.new_image = Image.new(mode="RGB", size=(self.image.width, self.image.height),
                                       color=self.ascii_background)
            self.new_draw = ImageDraw.Draw(self.new_image)

        except Exception as e:
            print('Unable to open image file', e)

    def convert_image(self):
        self.open_image()
        if self.image:
            if self.show_original:
                self.image.show()

            self.chunk_image()

            self.image.save(fp=get_full_filename(self.new_file_name))

            if self.show_final:
                self.image.show()

    # @timer_func
    def convert_video(self):
        image_counter = 0
        read_counter = 0

        print('Read file: {}'.format(self.file_name))
        video_in = cv2.VideoCapture(get_full_filename(self.file_name))  # ToDo: says we capture an image from a webcam
        frame_rate = int(video_in.get(5))

        # Below works for AVI
        # video_out = cv2.VideoWriter(get_full_filename(self.new_file_name), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
        #                             frame_rate, (int(video_in.get(3)), int(video_in.get(4))))

        # Below works for mp4 on desktop, but not in browser to play
        video_out = cv2.VideoWriter(get_full_filename(self.new_file_name), cv2.VideoWriter_fourcc(*'mp4v'), frame_rate,
                                    (int(video_in.get(3)), int(video_in.get(4))))

        print(f'Processing frame {read_counter:5d}', end='')
        while video_in.isOpened():
            ret, cv2_im = video_in.read()
            if ret and read_counter % self.frame_step == 0:
                print(f'\b\b\b\b\b{read_counter:5d}', end='')
                converted = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
                self.image = Image.fromarray(converted)

                # ToDo: the 3 class image variables need to be set more generically in chunk process
                self.pixels = self.image.load()

                if self.method == 'ascii':
                    self.new_image = Image.new(mode="RGB", size=(self.image.width, self.image.height),
                                               color=self.ascii_background)
                    self.new_draw = ImageDraw.Draw(self.new_image)

                self.chunk_image()

                pil_image = self.image.convert('RGB')
                open_cv_image = numpy.array(pil_image)
                open_cv_image = open_cv_image[:, :, ::-1].copy()

                video_out.write(open_cv_image)

                image_counter += 1
            elif not ret:
                break
            read_counter += 1

        video_in.release()
        video_out.release()

        print(f'\nsource frames={read_counter}, pyxelated frames={image_counter}')

    def convert_file(self):
        if self.file_name.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS:
            self.convert_image()
        else:
            self.convert_video()


if __name__ == '__main__':
    # P = PyxelArt(file_name='static/tmp/test1.png', method="ascii")  # Convert static image to ascii art
    P = PyxelArt(file_name='static/tmp/test2.mp4', method="ascii")  # Convert video file to ascii art

    P.convert_file()
