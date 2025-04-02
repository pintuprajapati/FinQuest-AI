from fastapi import Query
from pydantic import BaseModel
from typing import Any
from pydantic import BaseModel, Field

class SearchSchema(BaseModel):
    user_query: str = Query(..., min_length=1, max_length=100)
    user_id: Any
    