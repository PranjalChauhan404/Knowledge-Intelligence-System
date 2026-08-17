from app.services.document_parser import DocumentParser
from app.services.chunking_service import ChunkingService
from app.services.metadata_service import MetadataService

parser = DocumentParser()
chunker = ChunkingService()
metadata_service = MetadataService()

file_path = "data/test_documents/sample.txt"

documents = parser.parse(file_path)
chunks = chunker.split_documents(documents)

for index, chunk in enumerate(chunks):

    metadata = metadata_service.create_metadata(
        file_path,
        index
    )

    chunk.metadata.update(metadata)

print("Document processing successful!")
print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\nText:")
    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)