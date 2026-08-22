import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class S3Service:

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )

        self.bucket_name = os.getenv("S3_BUCKET_NAME")

    def upload_file(self, file_path, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_path)

        self.s3_client.upload_file(
            file_path,
            self.bucket_name,
            object_name
        )

        return f"s3://{self.bucket_name}/{object_name}"

    def download_file(self, object_name, file_path):
        self.s3_client.download_file(
            self.bucket_name,
            object_name,
            file_path
        )

    def delete_file(self, object_name):
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=object_name
        )