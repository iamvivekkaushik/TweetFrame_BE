from app.main import config

from app.database.core import SessionLocal
from app.frame.repository import FrameRepository
from app.frame.models import FrameUpdate

db = SessionLocal()


frame_repo = FrameRepository(db)
frames = frame_repo.get_all_frames()

count = 0

for frame in frames:
    print("-----------------------------")
    if config.B2_ENDPOINT in frame.url:
        print("Updating frame: {}".format(frame.id))
        new_url = frame.url.replace(config.B2_ENDPOINT, config.CDN_ENDPOINT)

        frame_update = FrameUpdate(url=new_url)
        frame_repo.update(object_id=frame.id, obj_in=frame_update)
        count += 1
    else:
        print("Skipping frame: {}".format(frame.id))
        print("Frame url: {}".format(frame.url))

    print("-----------------------------")

print("============================")
print("All {} frame URLs are updated.".format(count))
print("============================")
db.close()
