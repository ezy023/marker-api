import boto3
from botocore.client import Config
import uuid


def gen_signed_s3_image_post():
    bucket = "marker-photos"
    uuid_str = str(uuid.uuid4())
    key = "%s.jpeg" % uuid_str
    region = 'us-east-1'

    client = boto3.client('s3', region_name=region, config=Config(signature_version='s3v4'))

    data =  client.generate_presigned_post(bucket, key)
    print data
    return data
