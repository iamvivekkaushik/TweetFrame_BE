from app.main import config

from app.database.core import SessionLocal
from app.user.repository import UserRepository
from app.user.models import UserUpdate

db = SessionLocal()


user_repo = UserRepository(db)
users = user_repo.get_all_users()

count = 0

for user in users:
    print("-----------------------------")
    if config.B2_ENDPOINT in user.original_image:
        print("Updating frame: {}".format(user.id))
        print("Old url: {}".format(user.original_image))
        new_url = user.original_image.replace(config.B2_ENDPOINT, config.CDN_ENDPOINT)
        print("New url: {}".format(new_url))

        user_update = UserUpdate(original_image=new_url)
        user_repo.update(object_id=user.id, obj_in=user_update)
        count += 1
    else:
        print("Skipping user: {}".format(user.id))
        print("Old url: {}".format(user.original_image))

    print("-----------------------------")


print("============================")
print("Updated image for {} users.".format(count))
print("============================")
db.close()
