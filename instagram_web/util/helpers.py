from app import app
import boto3, botocore
from config import Config

s3 = boto3.client(
    "s3",
    aws_access_key_id = app.config["S3_KEY"],
    aws_secret_access_key = app.config["S3_SECRET"]
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            app.config.get("S3_BUCKET"),
            file.filename,
            ExtraArgs = {
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
