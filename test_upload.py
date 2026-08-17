from app.services.s3_service import S3Service

s3 = S3Service()

file_path = "data/test_document.txt"

result = s3.upload_file(file_path)

print("Upload successful!")
print(result)