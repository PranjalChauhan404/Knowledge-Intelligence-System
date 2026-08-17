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