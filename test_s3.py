from app.services.s3_service import S3Service

s3 = S3Service()

response = s3.s3_client.list_objects_v2(
    Bucket=s3.bucket_name
)

print("S3 connection successful!")
print("Bucket:", s3.bucket_name)