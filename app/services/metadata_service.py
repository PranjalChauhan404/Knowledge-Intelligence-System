import os
import uuid
import hashlib


class MetadataService:

    def create_document_id(self, file_path):
        with open(file_path, "rb") as file:
            file_hash = hashlib.sha256(file.read()).hexdigest()

        return str(uuid.uuid5(uuid.NAMESPACE_URL, file_hash))

    def create_metadata(
        self,
        file_path,
        chunk_index,
        document_id
    ):
        filename = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1].lower()

        return {
            "document_id": document_id,
            "filename": filename,
            "file_type": file_type,
            "source": file_path,
            "chunk_id": chunk_index
        }