import base64
import os
from io import BytesIO

from PIL import Image

import requests
from app import config
from app.frame.models import Frame
from app.user.models import User

import os.path

from fastapi import UploadFile, HTTPException, status

from app import config


def create_image_url(path: str) -> str:
    """
    Create image url
    """
    if path.startswith("http"):
        return path

    protocol = "https://"
    if config.ENVIRONMENT == "development":
        protocol = "http://"
    return protocol + config.DOMAIN + "/" + path


def validate_file(frame: UploadFile) -> int:
    # convert 300 kb into bytes
    max_allowed_size = 300 * 1024

    if frame.content_type != "image/png":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Frame must be a PNG file.",
        )
    file = frame.file
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    if file_size > max_allowed_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 300KB.",
        )
    file.seek(0, os.SEEK_SET)
    return file_size


def generate_frame_image(user: User, frame: Frame) -> str:
    """
    Returns the base 64 encoded image
    """
    background_url = user.original_image
    # frame_url = os.path.join(config.BASE_DIR, frame.url)
    frame_url = frame.url

    if not background_url:
        raise Exception("User doesn't have an image to use as background")

    response = requests.get(frame_url)
    frame_image = Image.open(BytesIO(response.content))
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
