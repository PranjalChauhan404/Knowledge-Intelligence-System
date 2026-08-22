from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class QueryRequest(BaseModel):

    query: str = Field(..., min_length=1, max_length=2000)

    collection: str = Field(
        default="default",
        min_length=1,
        max_length=100
    )

    conversation_id: Optional[str] = Field(
        default=None,
        max_length=100
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Query cannot be empty")

        return value

    @field_validator("collection")
    @classmethod
    def validate_collection(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Collection cannot be empty")

        return value

    @field_validator("conversation_id")
    @classmethod
    def validate_conversation_id(cls, value):
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class SourceModel(BaseModel):

    chunk_id: int
    document_id: str
    filename: str
    source: str


class QueryResponse(BaseModel):

    answer: str
    sources: List[SourceModel]
    conversation_id: Optional[str] = None