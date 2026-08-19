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

    chunks_deleted = vector_store.delete_document(
        collection_name,
        document_id
    )

    s3_uri = document["s3_uri"]

    bucket_name = s3_service.bucket_name

    object_name = s3_uri.split(
        f"s3://{bucket_name}/",
        1
    )[1]

    s3_service.s3_client.delete_object(
        Bucket=bucket_name,
        Key=object_name
    )

    registry_service.delete_document(
        document_id
    )

    return jsonify({
        "message": "Document deleted successfully",
        "document_id": document_id,
        "chunks_deleted": chunks_deleted
    })


@document_bp.route(
    "/documents/<document_id>/reindex",
    methods=["POST"]
)
def reindex_document(document_id):

    document = registry_service.get_document(document_id)

    if document is None:
        return jsonify({
            "error": "Document not found"
        }), 404

    s3_uri = document["s3_uri"]
    bucket_name = s3_service.bucket_name

    object_name = s3_uri.split(
        f"s3://{bucket_name}/",
        1
    )[1]

    filename = document["filename"]

    temp_directory = tempfile.mkdtemp()

    local_path = os.path.join(
        temp_directory,
        filename
    )

    try:

        # Download original document from S3
        s3_service.download_file(
            object_name,
            local_path
        )

        # Re-process document
        chunks_stored = ingestion_service.ingest(
            local_path,
            document["collection"]
        )

        # Update registry
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
            "details": str(error)
        }), 500

    finally:

        if os.path.exists(local_path):
            os.remove(local_path)

        if os.path.exists(temp_directory):
            os.rmdir(temp_directory)