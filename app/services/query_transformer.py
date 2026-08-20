class QueryTransformer:

    @staticmethod
    def transform(query: str) -> str:

        # Remove leading/trailing whitespace
        query = query.strip()

        # Collapse repeated whitespace
        query = " ".join(query.split())

        return query