# 행동 데이터 모델
from enum import Enum

from pydantic import BaseModel, Field

class AutonomousAction(str, Enum):
      IDLE = "idle"
      LOOK_AROUND = "look_around"
      SELF_TALK = "self_talk"
      REST = "rest"
      THINK = "think"

class AutonomyRequest(BaseModel):
      minutes_since_interaction: int = Field(
            default=0,
            ge=0,
            le=1440
      )

      energy: int = Field(
            default=80,
            ge=0,
            le=100
      )

      allow_self_talk: bool = True

class AutonomyResponse(BaseModel):
      action: AutonomousAction
      message: str
      reason: str