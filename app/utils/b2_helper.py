import time

from b2sdk.v2 import B2Api, InMemoryAccountInfo
from fastapi import UploadFile

from app.config import B2_APP_KEY, B2_KEY_ID, B2_BUCKET_NAME, B2_ENDPOINT
from app.file.models import FileCreate
from app.file.repository import FileRepository

info = InMemoryAccountInfo()

b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APP_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)


# create unique file name
def create_unique_file_name(path: str, extension: str) -> str:
    timestamp: str = str(int(time.time()))
    return f"{path}/twitpro_{timestamp}.{extension}"


def upload_file(db, file: UploadFile, path: str, file_size: int) -> str:
    file_path = create_unique_file_name(path, file.filename.split(".")[-1])
    content_type = file.content_type
    file_name = file_path.split("/")[-1]

    # Upload a new file
    bucket.upload_bytes(
        data_bytes=file.file.read(),
        file_name=file_path,
        content_type=file.content_type,
    )
    file_url = B2_ENDPOINT + file_path

    file_repo = FileRepository(db)
    file_create = FileCreate(name=file_name, url=file_url, path=file_path,
                             size=file_size, mimetype=content_type)

    file_repo.create(file_create)

    return file_url


def upload_frame(db, file: UploadFile, file_size: int) -> str:
    return upload_file(db=db, file=file, path="frame", file_size=file_size)
