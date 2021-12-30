import os.path
from pathlib import Path

from fastapi import UploadFile, HTTPException, status

from PIL import ImageFile
import shutil

from app.config import BASE_DIR



def validate_file(frame: UploadFile):
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


def save_image(frame: UploadFile, path: str = "media/frames"):
    """
    Save image to file
    """
    media_folder = os.path.join(BASE_DIR, path)
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)

    file = frame.file
    file_name = frame.filename
    frame_path = Path(os.path.join(media_folder, file_name))

    with frame_path.open("wb") as buffer:
        shutil.copyfileobj(file, buffer)

    frame.file.close()
    return path + "/" + file_name
