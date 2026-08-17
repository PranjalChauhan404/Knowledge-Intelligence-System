import os
import uuid


class MetadataService:

    def create_document_id(self):
        return str(uuid.uuid4())

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