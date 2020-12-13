from .models import Image
from base64 import b64decode
from flask import current_app, abort
from google.cloud import storage
from io import BytesIO
from mimetypes import guess_extension, guess_type
from PIL import Image as PILImage
from re import sub
from secrets import token_urlsafe
from werkzeug.utils import secure_filename


def upload(sql_entity, images):
    gcs = storage.Client()
    bucket = gcs.get_bucket(current_app.config.get("GCS_BUCKET"))
    for image in images:
        try:
            ext = guess_extension(guess_type(image)[0])[1:]
            filename = secure_filename(f"{token_urlsafe(32)}.{ext}")
            image_string = sub("^data:image/.+;base64,", "", image)
            byte_image = b64decode(image_string)
            pil_image = PILImage.open(BytesIO(byte_image))
            pil_image.save(f"{current_app.instance_path}/{filename}")
            blob = bucket.blob(filename)
            policy = bucket.get_iam_policy(requested_policy_version=3)
            policy.bindings.append({
                "role": "roles/storage.objectViewer",
                "members": {"allUsers"}
            })
            bucket.set_iam_policy(policy)
            blob.upload_from_filename(
                f"{current_app.instance_path}/{filename}")
            sql_entity.images.append(Image(url=blob.public_url))
        except:
            abort(500)