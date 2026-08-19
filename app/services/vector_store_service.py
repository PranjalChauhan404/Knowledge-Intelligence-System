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

        collection.upsert(
            ids=ids,
            documents=[doc.page_content for doc in documents],
            embeddings=embeddings,
            metadatas=[doc.metadata for doc in documents]
        )

        return len(documents)

    def search(
        self,
        collection_name,
        query_embedding,
        top_k=5,
        similarity_threshold=1.6
    ):
        collection = self.get_collection(collection_name)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        filtered_results = {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

        for i, distance in enumerate(results["distances"][0]):

            if distance <= similarity_threshold:
                filtered_results["documents"][0].append(
                    results["documents"][0][i]
                )

                filtered_results["metadatas"][0].append(
                    results["metadatas"][0][i]
                )

                filtered_results["distances"][0].append(
                    distance
                )

        return filtered_results

    def delete_document(
        self,
        collection_name,
        document_id
    ):
        collection = self.get_collection(collection_name)

        results = collection.get(
            where={
                "document_id": document_id
            }
        )

        ids = results["ids"]

        if ids:
            collection.delete(ids=ids)

        return len(ids)

    def list_collections(self):
        return self.client.list_collections()

    def create_collection(self, collection_name):
        return self.client.get_or_create_collection(
            name=collection_name
        )

    def delete_collection(self, collection_name):
        self.client.delete_collection(
            name=collection_name
        )