from PIL import Image, ImageDraw, ImageFont, ImageTk
from time import time
import cv2
import numpy
import os
import sys


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


def convert_to_gray(rgb):
    return int(0.2989 * rgb[0] + 0.5870 * rgb[1] + 0.1140 * rgb[2])


class Pixelate:
    def __init__(self, width=128, height=72, method='pixelate', show_original=False, file_name=''):
        self.width = width
        self.height = height
        self.method = method
        self.show_original = show_original
        self.file_name = file_name
        self.new_file_name = f"{file_name.rsplit('.', 1)[0]}-{self.method}.avi"

        self.ascii_table = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        self.ascii_chunks = 256 / len(self.ascii_table)

        self.font_size = 20  # ToDo: Need to change based on chunk size, 20 works in my image test
        self.ascii_font = ImageFont.truetype('fonts/10980_Decoder.ttf', self.font_size)
        self.text_color = (24, 242, 18)  # Matrix green
        self.ascii_background = (0, 0, 0)

        self.frame_step = 4

        self.image = None
        self.pixels = None
        self.draw = None
        self.new_image = None
        self.new_draw = None

    @timer_func
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

                # Pixelate default
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

                # for pixelate and greyscale
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
            self.image = Image.open(self.file_name)
            self.pixels = self.image.load()
            self.draw = ImageDraw.Draw(self.image)
            self.new_image = Image.new(mode="RGB", size=(self.image.width, self.image.height),
                                       color=self.ascii_background)
            self.new_draw = ImageDraw.Draw(self.new_image)

        except Exception as e:
            print('Unable to open image file', e)

    def convert_image(self, show=True):
        self.open_image()
        if self.image:
            if self.show_original:
                self.image.show()

            self.chunk_image()

            if show:
                self.image.show()

    def convert_video(self):
        image_counter = 0
        read_counter = 0

        print('Read file: {}'.format(self.file_name))
        cap = cv2.VideoCapture(self.file_name)  # says we capture an image from a webcam
        out = cv2.VideoWriter(self.new_file_name, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                              (int(cap.get(3)), int(cap.get(4))))

        while cap.isOpened():
            ret, cv2_im = cap.read()
            if ret and read_counter % self.frame_step == 0:
                print(f'Processing frame {read_counter}')
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

                out.write(open_cv_image)

                image_counter += 1
            elif not ret:
                break
            read_counter += 1

        cap.release()
        out.release()

        print(f'image={image_counter}, read={read_counter}')


if __name__ == '__main__':
    # # Convert static image to ascii art
    # P = Pixelate(file_name='assets/test1.png', method="ascii")
    # P.convert_image()

    # Convert video file to ascii art
    P = Pixelate(file_name='assets/test2.mp4', method="ascii")
    P.convert_video()
