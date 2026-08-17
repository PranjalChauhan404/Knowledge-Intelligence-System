from app.services.document_parser import DocumentParser
from app.services.chunking_service import ChunkingService

parser = DocumentParser()
chunker = ChunkingService()

documents = parser.parse("data/test_documents/sample.txt")

chunks = chunker.split_documents(documents)

print("Original documents:", len(documents))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)