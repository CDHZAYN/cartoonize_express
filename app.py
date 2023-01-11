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
if opts['colab-mode']:
    from flask_ngrok import run_with_ngrok #to run the application on colab using ngrok


from cartoonize import WB_Cartoonize

if not opts['run_local']:
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        from gcloud_utils import upload_blob, generate_signed_url, delete_blob, download_video
    else:
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")
    from video_api import api_request
    # Algorithmia (GPU inference)
    import Algorithmia

## Init Cartoonizer and load its weights 
wb_cartoonizer = WB_Cartoonize(os.path.abspath("white_box_cartoonizer/saved_models/"), opts['gpu'])

def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def cartoonize(img):
        try:
#             if flask.request.files.get('image'):
#                 img = flask.request.files["image"].read()
                
                ## Read Image and convert to PIL (RGB) if RGBA convert appropriately
                image = convert_bytes_to_image(img)

                img_name = str(uuid.uuid4())
                
                cartoon_image = wb_cartoonizer.infer(image)
                
                cartoonized_img_name = os.path.join('./static/cartoonized_images/', img_name + ".jpg")
                cv2.imwrite(cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))

                # Upload to bucket
                output_uri = upload_blob("cartoonized_images", cartoonized_img_name, img_name + ".jpg", content_type='image/jpg')

                # Delete locally stored cartoonized image
                os.system("rm " + cartoonized_img_name)
                cartoonized_img_name = generate_signed_url(output_uri)

                return true
        except Exception:
            print(traceback.print_exc())

if __name__ == "__main__":
        cartoonize(sys.argv[0])