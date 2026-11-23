from fastapi import FastAPI

# 감정 import
from app.emotion.engine import emotion_engine
from app.emotion.models import EmotionUpdateRequest

# 기억 import
from app.memory.engine import memory_engine
from app.memory.models import MemoryRequest

# 관계 import
from app.relationship.engine import relationship_engine
from app.relationship.models import RelationshipUpdateRequest
from app.personality.profile import (
      get_personality,
      get_personality_prompt
)

# 자율행동 import
from app.autonomy.engine import autonomy_engine
from app.autonomy.models import AutonomyRequest

# 통합제어 import
from app.orchestrator.service import ai_orchestrator
from app.orchestrator.models import ChatRequest

app = FastAPI (
      title = "Jay AI",
      description = "감정이 있는 가상의 인간 AI 엔진",
      version = "0.1.0"
)

@app.get("/")
async def root():
      return {
            "status": "success",
            "message": "Jay AI Engine is running"
      }

@app.get("/healthy")
async def health():
      return {
            "status": "healthy",
            "service": "AI Virtual Human",
            "version": "0.1.0"
      }

# 1. AI 성격
@app.get("/api/personality")
async def personality():
      profile = get_personality()

      return profile.model_dump()

@app.get("/api/personality/prompt")
async def personality_prompt():
      profile = get_personality()

      return {
            "character_id": profile.character_id,
            "prompt": get_personality_prompt(profile)
      }

# 2. AI 감정
@app.get("/api/emotion")
async def get_emotion():
      return emotion_engine.get_state().model_dump()

@app.post("/api/emotion/update")
async def update_emotion(request: EmotionUpdateRequest):
      state = emotion_engine.update(request.text)

      return {
            "status": "success",
            "emotion": state.model_dump()
      }

@app.post("/api/emotion/reset")
async def reset_emotion():
      state = emotion_engine.reset()

      return {
            "status": "success",
            "emotion": state.model_dump()
      }

# 3. AI 메모리(기억)
@app.post("/api/memory")
async def save_memory(request: MemoryRequest):
      memory = memory_engine.save_memory(
            request.user_message,
            request.ai_response
      )

      return {
            "status": "success",
            "memory": memory.model_dump(mode="json")
      }

@app.get("/api/memory")
async def get_memories(limit: int = 10):
      limit = max(1, min(limit, 100))

      memories = memory_engine.get_recent_memories(limit)

      return {
            "count": len(memories),
            "memories": [
                  memory.model_dump(mode="json")
                  for memory in memories
            ]
      }

@app.get("/api/memory/search")
async def search_memories(keyword: str):
      memories = memory_engine.search_memories(keyword)

      return {
            "count": len(memories),
            "memories": [
                  memory.model_dump(mode="json")
                  for memory in memories
            ]
      }

@app.delete("/api/memory")
async def clear_memories():
      memory_engine.clear_memories()

      return {
            "status": "success",
            "message": "모든 메모리가 삭제되었습니다."
      }


# 4. AI 관계
@app.get("/api/relationship")
async def get_relationship():
      state = relationship_engine.get_state()

      return {
            "status": "success",
            "relationship": state.model_dump(mode="json")
      }

@app.post("/api/relationship/update")
async def update_relationship(request: RelationshipUpdateRequest):
      state = relationship_engine.update(request.event)

      return {
            "status": "success",
            "relationship": state.model_dump(mode="json")
      }

@app.post("/api/relationship/reset")
async def reset_relationship():
      state = relationship_engine.reset()

      return {
            "status": "success",
            "relationship": state.model_dump(mode="json")
      }

# 5. AI 자율행동
@app.post("/api/autonomy/decide")
async def decide_autonomous_action(request: AutonomyRequest):
      result = autonomy_engine.decide(request)

      return {
            "status": "success",
            "action": result.action.value,
            "message": result.message,
            "reason": result.reason
      }

# 6. 통합 제어 엔진
@app.post("/api/chat")
async def chat(request: ChatRequest):
      result = ai_orchestrator.process_message(
            request.message
      )

      return {
            "status": "success",
            **result
      }