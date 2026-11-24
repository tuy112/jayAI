# 통합 제어 엔진
# 지금까지 만든 5개의 엔진을 하나로 연결하는 작업
# Personality, Emotion, Memory, Relationship, Autonomy 통합

from app.orchestrator.llm_service import generate_reply

from app.personality.profile import (
      get_personality,
      get_personality_prompt
)

from app.emotion.engine import emotion_engine
from app.memory.engine import memory_engine
from app.relationship.engine import relationship_engine

class AIOrchestrator:
      async def process_message(self, message: str):
            
            # 1. 캐릭터 성격 확인
            personality = get_personality()
            personality_prompt = get_personality_prompt(
                  personality
            )

            # 2. 현재 감정 업데이트
            emotion = emotion_engine.update(message)
            emotion_data = emotion.model_dump()

            # 3. 과거 기억 검색
            words = message.split()
            keyword = max(words, key=len) if words else ""

            memories = (
                  memory_engine.search_memories(keyword)
                  if len(keyword) >= 2
                  else []
            )
            memories_data = [
                  memory.model_dump(mode="json")
                  for memory in memories
            ]

            # 4. 최근 대화 기억
            recent_memories = memory_engine.get_recent_memories(5)
            recent_memories_data = [
                  memory.model_dump(mode="json")
                  for memory in recent_memories
            ]

            # 5. 사용자와의 관계 확인
            relationship = relationship_engine.get_state()
            relationship_data = relationship.model_dump(
                  mode="json"
            )

            # 6. 로컬 LLM 응답 생성
            reply = await generate_reply(
                  personality_prompt=personality_prompt,
                  emotion=emotion_data,
                  relationship=relationship_data,
                  memories=memories_data,
                  user_message=message
            )

            # 7. 대화 기억 저장
            memory_engine.save_memory(
                  user_message=message,
                  ai_response=reply
            )

            # 8. 결과 반환
            return {
                  "character_name": personality.name,
                  "reply": reply,
                  "emotion": emotion_data,
                  "relationship": relationship_data,
                  "memories": memories_data,
                  "recent_memories": recent_memories_data,
                  "personality_prompt": personality_prompt,
                  "mode": "local"
            }

ai_orchestrator = AIOrchestrator()