from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
      message: str = Field(min_length=1, max_length=5000)

class ChatResponse(BaseModel):
      character_name: str
      reply: str
      emotion: dict
      relationship: dict
      memories: list
      mode: str