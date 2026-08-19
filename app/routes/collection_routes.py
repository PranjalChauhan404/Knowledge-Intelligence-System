from flask import Blueprint, request, jsonify

from app.services.vector_store_service import VectorStoreService


collection_bp = Blueprint("collections", __name__)

vector_store = VectorStoreService()


@collection_bp.route("/collections", methods=["GET"])
def get_collections():

    collections = vector_store.list_collections()

    return jsonify({
        "collections": [
            collection.name
            for collection in collections
        ]
    })


@collection_bp.route("/collections", methods=["POST"])
def create_collection():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    collection_name = data.get("name")

    if not collection_name:
        return jsonify({
            "error": "Collection name is required"
        }), 400

    collection = vector_store.create_collection(
        collection_name
    )

    return jsonify({
        "message": "Collection created successfully",
        "collection": collection.name
    }), 201


@collection_bp.route(
    "/collections/<collection_name>",
    methods=["DELETE"]
)
def delete_collection(collection_name):

    try:

        vector_store.delete_collection(
            collection_name
        )

        return jsonify({
            "message": "Collection deleted successfully",
            "collection": collection_name
        })

    except Exception:

        return jsonify({
            "error": "Collection not found"
        }), 404