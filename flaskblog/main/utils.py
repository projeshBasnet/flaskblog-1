import secrets
import os
from PIL import Image
from flaskblog import app

# Utility function for saving pictures
def save_pic(pic_data, img_location):
    randomname = secrets.token_hex(8)
    _, ext_name = os.path.splitext(pic_data.filename)
    pic_name = randomname + ext_name
    pic_path = os.path.join(app.root_path,f'static/img/{img_location}', pic_name)
    if img_location == 'profile_pics':
        output_size  =(30, 30)
    else:
        output_size = (200,200)    
    i = Image.open(pic_data)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_name