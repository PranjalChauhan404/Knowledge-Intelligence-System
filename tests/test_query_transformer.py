from app.services.query_transformer import QueryTransformer


def test_query_transformer():
    query = "   what   is   RAG?   "

    result = QueryTransformer.transform(query)

    assert result == "what is RAG?"