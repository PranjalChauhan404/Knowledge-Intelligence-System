import pytest
from pydantic import ValidationError

from app.models.api_models import QueryRequest


def test_valid_query_request():

    request = QueryRequest(
        query="What is RAG?",
        collection="default"
    )

    assert request.query == "What is RAG?"
    assert request.collection == "default"


def test_empty_query_rejected():

    with pytest.raises(ValidationError):

        QueryRequest(
            query=""
        )