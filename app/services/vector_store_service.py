import chromadb
import os


class VectorStoreService:

    def __init__(self):
        persist_directory = os.path.join("data", "chroma")

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

    def get_collection(self, collection_name="default"):
        return self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(
        self,
        collection_name,
        documents,
        embeddings
    ):
        collection = self.get_collection(collection_name)

        ids = [
            f"{doc.metadata['document_id']}_{doc.metadata['chunk_id']}"
            for doc in documents
        ]

        collection.add(
            ids=ids,
            documents=[doc.page_content for doc in documents],
            embeddings=embeddings,
            metadatas=[doc.metadata for doc in documents]
        )

        return len(documents)