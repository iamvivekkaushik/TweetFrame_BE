import base64
import os
from io import BytesIO

from PIL import Image

import requests
from app import config
from app.frame.models import Frame
from app.user.models import User


def generate_frame_image(user: User, frame: Frame) -> str:
    """
    Returns the base 64 encoded image
    """
    background_url = user.original_image
    frame_url = os.path.join(config.BASE_DIR, frame.url)

    frame_image = Image.open(frame_url, "r")
    frame_image = frame_image.convert("RGBA")

    frame_w, frame_h = frame_image.size

    response = requests.get(background_url)
    background = Image.open(BytesIO(response.content))
    bg_w, bg_h = background.size

    if frame_w != bg_w:
        frame_image = frame_image.resize((bg_w, bg_w))

    background.paste(frame_image, (0, 0), frame_image)

    buffered = BytesIO()
    background.convert("RGB").save(buffered, format="jpeg", quality=95)
    img_str = base64.b64encode(buffered.getvalue())

    return img_str.decode("utf-8")
