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
