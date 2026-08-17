from app.services.ingestion_service import IngestionService

ingestion = IngestionService()

count = ingestion.ingest(
    "data/test_documents/sample.txt",
    "separation_test"
)

print("Ingestion successful!")
print("Chunks stored:", count)