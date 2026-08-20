from pydantic import BaseModel, Field
from typing import List, Optional


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    collection: str = "default"
    conversation_id: Optional[str] = None


class SourceModel(BaseModel):
    chunk_id: int
    document_id: str
    filename: str
    source: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceModel]
    conversation_id: Optional[str] = None