import base64
from io import BytesIO

import mozjpeg_lossless_optimization as mozjpg
import numpy as np
from PIL import Image


def base64_to_numpy(b64_img):
    """
    Convert a base64 image to a numpy array.

    Arguments: b64_img -- Base64 encoded image.
    Return: Numpy array.
    """

    img_bytes = base64.b64decode(b64_img)
    img_file = BytesIO(img_bytes)
    img_pil = Image.open(img_file)
    img_np = np.asarray(img_pil)
    return img_np


def resize_image(img: Image):
    width = img.size[0]
    height = img.size[1]
    if ((width >= height) and (width >= 800)):
        mult = 800 / width
        new_width = int(mult * width)
        new_height = int(mult * height)
        img_resize = img.resize((new_width, new_height))
        return img_resize
    if ((width < height) and (height >= 800)):
        mult = 800 / height
        new_width = int(mult * width)
        new_height = int(mult * height)
        img_resize = img.resize((new_width, new_height))
        return img_resize
    else:
        img_resize = img.resize((width, height))
        return img_resize


def optimize_img(image_pillow):
    img = resize_image(image_pillow)
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    byte_img = buffer.getvalue()
    optimized_img = mozjpg.optimize(byte_img)
    return optimized_img
