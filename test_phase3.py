from app.services.document_parser import DocumentParser
from app.services.chunking_service import ChunkingService
from app.services.metadata_service import MetadataService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


FILE_PATH = "data/test_documents/sample.txt"
COLLECTION = "phase3_test"


parser = DocumentParser()

chunker = ChunkingService(
    chunk_size=150,
    chunk_overlap=30
)

metadata_service = MetadataService()
embedding_service = EmbeddingService()
vector_store = VectorStoreService()


# 1. Parse
documents = parser.parse(FILE_PATH)

# 2. Chunk
chunks = chunker.split_documents(documents)

# 3. Create ONE document ID
document_id = metadata_service.create_document_id()

# 4. Add metadata to every chunk
for index, chunk in enumerate(chunks):

    metadata = metadata_service.create_metadata(
        FILE_PATH,
        index,
        document_id
    )

    chunk.metadata.update(metadata)


# 5. Create embeddings
texts = [chunk.page_content for chunk in chunks]

embeddings = embedding_service.embed_documents(texts)


# 6. Store in ChromaDB
stored = vector_store.add_documents(
    COLLECTION,
    chunks,
    embeddings
)

print(f"Chunks stored: {stored}")


# 7. User query
query = input("\nAsk a question: ")

query_embedding = embedding_service.embed_query(query)


# 8. Retrieve
results = vector_store.search(
    collection_name=COLLECTION,
    query_embedding=query_embedding,
    top_k=3,
    similarity_threshold=1.6
)


# 9. Display results
print("\nRelevant results:")

for i, document in enumerate(results["documents"][0]):

    print(f"\n--- Result {i + 1} ---")
    print(document)

    print("Distance:", results["distances"][0][i])

    print("Metadata:", results["metadatas"][0][i])