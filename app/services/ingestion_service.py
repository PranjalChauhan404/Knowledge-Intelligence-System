from app.services.document_parser import DocumentParser
from app.services.chunking_service import ChunkingService
from app.services.metadata_service import MetadataService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService


class IngestionService:

    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = ChunkingService(
            chunk_size=150,
            chunk_overlap=30
        )
        self.metadata_service = MetadataService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()

    def ingest(self, file_path, collection_name):

        documents = self.parser.parse(file_path)

        chunks = self.chunker.split_documents(documents)

        document_id = self.metadata_service.create_document_id(file_path)

        for index, chunk in enumerate(chunks):

            metadata = self.metadata_service.create_metadata(
                file_path,
                index,
                document_id
            )

            chunk.metadata.update(metadata)

        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.embedding_service.embed_documents(texts)

        return self.vector_store.add_documents(
            collection_name,
            chunks,
            embeddings
        )