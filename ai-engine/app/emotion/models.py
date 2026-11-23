from pydantic import BaseModel, Field


class EmotionState(BaseModel):
      happiness: int = Field(default=50, ge=0, le=100)
      sadness: int = Field(default=10, ge=0, le=100)
      anger: int = Field(default=0, ge=0, le=100)
      curiosity: int = Field(default=50, ge=0, le=100)
      loneliness: int = Field(default=10, ge=0, le=100)
      anxiety: int = Field(default=10, ge=0, le=100)


class EmotionUpdateRequest(BaseModel):
      text: str