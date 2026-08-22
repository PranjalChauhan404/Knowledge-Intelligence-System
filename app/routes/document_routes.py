from flask import Blueprint, jsonify
import os
import tempfile

from app.services.document_registry_service import DocumentRegistryService
from app.services.vector_store_service import VectorStoreService
from app.services.s3_service import S3Service
from app.services.ingestion_service import IngestionService


document_bp = Blueprint("documents", __name__)

registry_service = DocumentRegistryService()
vector_store = VectorStoreService()
s3_service = S3Service()
ingestion_service = IngestionService()


@document_bp.route("/documents", methods=["GET"])
def get_documents():

    documents = registry_service.get_all_documents()

    return jsonify({
        "documents": documents
    })


@document_bp.route("/documents/<document_id>", methods=["GET"])
def get_document(document_id):

    document = registry_service.get_document(document_id)

    if document is None:
        return jsonify({
            "error": "Document not found"
        }), 404

    return jsonify(document)


@document_bp.route("/documents/<document_id>", methods=["DELETE"])
def delete_document(document_id):

    document = registry_service.get_document(document_id)

    if document is None:
        return jsonify({
            "error": "Document not found"
        }), 404

    collection_name = document["collection"]
    s3_uri = document["s3_uri"]

    try:

        # ------------------------------------------
        # 1. Delete document chunks from vector store
        # ------------------------------------------

        chunks_deleted = vector_store.delete_document(
            collection_name,
            document_id
        )

        # ------------------------------------------
        # 2. Delete original document from S3
        # ------------------------------------------

        bucket_name = s3_service.bucket_name

        prefix = f"s3://{bucket_name}/"

        if not s3_uri.startswith(prefix):
            raise ValueError(
                "Invalid S3 URI for document"
            )

        object_name = s3_uri.split(
            prefix,
            1
        )[1]

        s3_service.s3_client.delete_object(
            Bucket=bucket_name,
            Key=object_name
        )

        # ------------------------------------------
        # 3. Remove document from registry
        # ------------------------------------------

        registry_service.delete_document(
            document_id
        )

        # ------------------------------------------
        # 4. Success
        # ------------------------------------------

        return jsonify({
            "message": "Document deleted successfully",
            "document_id": document_id,
            "chunks_deleted": chunks_deleted
        })

    except Exception as error:

        # IMPORTANT:
        # Registry is NOT deleted if any previous
        # operation fails. This allows the user to
        # retry the deletion instead of losing the
        # registry record.

        print(
            f"Document deletion failed: {error}"
        )

        return jsonify({
            "error": "Document deletion failed",
            "message": (
                "The document could not be completely "
                "removed. Please try again."
            )
        }), 500


@document_bp.route(
    "/documents/<document_id>/reindex",
    methods=["POST"]
)
def reindex_document(document_id):

    document = registry_service.get_document(
        document_id
    )

    if document is None:
        return jsonify({
            "error": "Document not found"
        }), 404

    s3_uri = document["s3_uri"]
    bucket_name = s3_service.bucket_name

    prefix = f"s3://{bucket_name}/"

    if not s3_uri.startswith(prefix):
        return jsonify({
            "error": "Invalid S3 URI for document"
        }), 500

    object_name = s3_uri.split(
        prefix,
        1
    )[1]

    filename = document["filename"]

    temp_directory = tempfile.mkdtemp()

    local_path = os.path.join(
        temp_directory,
        filename
    )

    try:

        # ------------------------------------------
        # 1. Download original document from S3
        # ------------------------------------------

        s3_service.download_file(
            object_name,
            local_path
        )

        # ------------------------------------------
        # 2. Re-process document
        # ------------------------------------------

        chunks_stored = ingestion_service.ingest(
            local_path,
            document["collection"]
        )

        # ------------------------------------------
        # 3. Update registry only after success
        # ------------------------------------------

        registry_service.update_document(
            document_id,
            {
                "status": "indexed",
                "chunk_count": chunks_stored
            }
        )

        return jsonify({
            "message": "Document re-indexed successfully",
            "document_id": document_id,
            "chunks_stored": chunks_stored,
            "status": "indexed"
        })

    except Exception as error:

        registry_service.update_document(
            document_id,
            {
                "status": "failed"
            }
        )

        return jsonify({
            "error": "Re-indexing failed",
        }), 500

    finally:

        if os.path.exists(local_path):

            try:
                os.remove(local_path)
            except OSError:
                pass

        if os.path.exists(temp_directory):

            try:
                os.rmdir(temp_directory)
            except OSError:
                pass