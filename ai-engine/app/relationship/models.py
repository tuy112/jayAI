from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field

class RelationshipEvent(str, Enum):
      POSITIVE = "positive"
      SUPPORTIVE = "supportive"
      PROMISE_KEPT = "promise_kept"
      CONFLICT = "conflict"
      APOLOGY = "apology"
      NEUTRAL = "neutral"

class RelationshipState(BaseModel):
      familiarity: int = Field(default=10, ge=0, le=100)
      trust: int = Field(default=20, ge=0, le=100)
      affection: int = Field(default=10, ge=0, le=100)
      respect: int = Field(default=30, ge=0, le=100)

      interaction_count: int = 0

      created_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc)
      )

      updated_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc)
      )

class RelationshipUpdateRequest(BaseModel):
      event: RelationshipEvent