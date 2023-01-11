import os
import io
import uuid
import sys
import yaml
import traceback

with open('./config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)

sys.path.insert(0, './white_box_cartoonizer/')

import cv2
from PIL import Image
import numpy as np
import skvideo.io

from cartoonize import WB_Cartoonize

## Init Cartoonizer and load its weights
wb_cartoonizer = WB_Cartoonize(os.path.abspath("white_box_cartoonizer/saved_models/"), opts['gpu'])

def convert_image(img):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """

#     pil_image = Image.open(io.BytesIO(img_bytes))
    pil_image = Image.fromarray(img.astype('uint8')).convert('RGB')
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')

    image = np.array(image)

    return image

def cartoonize(img_name):
    try:
        path = os.path.join('./static/uploaded_images/', img_name)
        image = cv2.imread(path)
        image = convert_image(image)
        cartoon_image = wb_cartoonizer.infer(image)
        cartoonized_img_name = os.path.join('./static/cartoonized_images/', img_name + ".jpg")
        cv2.imwrite(cartoonized_img_name, cartoon_image)
        print("done", file=sys.stdout)
        return
    except Exception:
        print(traceback.print_exc(), file=sys.stderr)

if __name__ == "__main__":
    cartoonize(sys.argv[1])