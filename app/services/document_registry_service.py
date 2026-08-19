import json
import os
from datetime import datetime


class DocumentRegistryService:

    def __init__(self):
        self.registry_path = "data/documents.json"

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w") as file:
                json.dump([], file)

    def get_all_documents(self):
        with open(self.registry_path, "r") as file:
            return json.load(file)

    def get_document(self, document_id):
        documents = self.get_all_documents()

        for document in documents:
            if document["document_id"] == document_id:
                return document

        return None

    def add_document(self, document):
        documents = self.get_all_documents()

        documents.append(document)

        with open(self.registry_path, "w") as file:
            json.dump(documents, file, indent=4)

    def delete_document(self, document_id):
        documents = self.get_all_documents()

        updated_documents = [
            document
            for document in documents
            if document["document_id"] != document_id
        ]

        with open(self.registry_path, "w") as file:
            json.dump(updated_documents, file, indent=4)

    def update_document(self, document_id, updates):
        documents = self.get_all_documents()

        for document in documents:
            if document["document_id"] == document_id:
                document.update(updates)

        with open(self.registry_path, "w") as file:
            json.dump(documents, file, indent=4)