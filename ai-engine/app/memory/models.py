# 기억 데이터 모델
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class MemoryRequest(BaseModel):
      user_message: str = Field(min_length=1)
      ai_response: str = Field(min_length=1)

class MemoryRecord(BaseModel):
      memory_id: str
      user_message: str
      ai_response: str
      created_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc)
      )