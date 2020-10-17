import re
from math import trunc
from os import listdir
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger
from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
import os
from moviepy.editor import *
from PIL import Image


def save_thumbnail_at_second(clip, second):
    file_name = os.path.basename(clip.filename)
    duration = trunc(clip.duration)
    max_duration = duration + 1
    if second < max_duration:
        frame = clip.get_frame(second)
    else:
        frame = clip.get_frame(duration)
    new_image_file_path = os.path.join(thumbnails_dir, f"{file_name}@{second}.jpg")
    new_image = Image.fromarray(frame)
    new_image.save(new_image_file_path)


def make_thumbnails(clip, number_of_thumbnails):
    duration = trunc(clip.duration)
    initial_offset = 3
    final_offset = duration - 3
    print(f"Max duration: {duration} | Number of thumbnails: {number_of_thumbnails}")
    step = trunc(duration / number_of_thumbnails)
    if duration > initial_offset and duration > final_offset and (duration + 6) >= step:
        for i in range(initial_offset, final_offset, step):
            print(f"Made thumbnail at second {i}")
            save_thumbnail_at_second(clip, i)
        print("End")
    else:
        print(f"Error, file duration ({duration}s) is too small to create {number_of_thumbnails} thumbnails")


# Main program
open_window = Tk()
open_window.withdraw()
filename = askopenfilename()
if filename:
    new_thumbnails_dir = re.split('\.[A-Za-z0-9]{3}$', os.path.basename(filename))[0]
    print(new_thumbnails_dir)
    thumbnails_dir = os.path.join(SAMPLE_OUTPUTS, Path(f"thumbnails/{new_thumbnails_dir}-thumbnails"))
    os.makedirs(thumbnails_dir, exist_ok=True)
    video = VideoFileClip(filename)
    no_thumbnails = int(askinteger("Thumbnails", "How many thumbnails would you like?"))
    make_thumbnails(video, no_thumbnails)
    os.startfile(thumbnails_dir)
