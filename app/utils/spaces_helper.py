import time
from io import BytesIO

import boto3
import requests
from PIL import Image
from fastapi import UploadFile

from app.config import (
    S3_BUCKET_NAME,
    S3_ACCESS_KEY_ID,
    S3_SECRET_ACCESS_KEY,
    S3_ENDPOINT,
)
from app.file.models import FileCreate
from app.file.repository import FileRepository


client = boto3.client(
    "s3",
    region_name="SGP1",
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)


# create unique file name
def create_unique_file_name(path: str, extension: str) -> str:
    timestamp: str = str(int(time.time()))
    return f"{path}/twitpro_{timestamp}.{extension}"


def upload_file(db, file: UploadFile, path: str, file_size: int) -> str:
    file_path = create_unique_file_name(path, file.filename.split(".")[-1])
    content_type = file.content_type
    file_name = file_path.split("/")[-1]

    # Upload a new file
    client.put_object(
        Body=file.file.read(),
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        ContentType=content_type,
    )

    file_url = S3_ENDPOINT + file_path

    file_repo = FileRepository(db)
    file_create = FileCreate(
        name=file_name,
        url=file_url,
        path=file_path,
        size=file_size,
        mimetype=content_type,
    )

    file_repo.create(file_create)

    return file_url


def upload_image_from_url(db, url: str, path: str, file_size: int = 300) -> str:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")

    buffered = BytesIO()
    img.convert("RGB").save(buffered, format="jpeg", quality=100)

    file_path = create_unique_file_name(path, "jpeg")
    file_name = file_path.split("/")[-1]

    # content_type = image.format
    content_type = "image/jpeg"
    # read bytes from pil image
    data = buffered.getvalue()
    client.put_object(
        Body=data,
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        ContentType=content_type,
    )

    file_url = S3_ENDPOINT + file_path

    file_repo = FileRepository(db)
    file_create = FileCreate(
        name=file_name,
        url=file_url,
        path=file_path,
        size=file_size,
        mimetype=content_type,
    )

    file_repo.create(file_create)
    return file_url


def upload_frame(db, file: UploadFile, file_size: int) -> str:
    return upload_file(db=db, file=file, path="frame", file_size=file_size)
