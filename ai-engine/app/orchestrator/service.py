# 통합 제어 엔진
# 지금까지 만든 5개의 엔진을 하나로 연결하는 작업
from app.personality.profile import (
      get_personality,
      get_personality_prompt
)

from app.emotion.engine import emotion_engine
from app.memory.engine import memory_engine
from app.relationship.engine import relationship_engine

class AIOrchestrator:
      def process_message(self, message: str):
            # 1. 캐릭터 성격 확인
            personality = get_personality()
            personality_prompt = get_personality_prompt(
                  personality
            )

            # 2. 현재 감정 업데이트
            emotion = emotion_engine.update(message)

            # 3. 과거 기억 검색
            words = message.split()
            keyword = max(words, key=len) if words else ""

            memories = (
                  memory_engine.search_memories(keyword)
                  if len(keyword) >= 2
                  else []
            )

            # 4. 최근 대화 기억
            recent_memories = memory_engine.get_recent_memories(5)

            # 5. 사용자와의 관계 확인
            relationship = relationship_engine.get_state()

            # 6. 현재 감정 확인
            emotion_data = emotion.model_dump()

            # 7. 임시 응답 생성
            # 다음 단계에서 GPT API 호출로 교체
            reply = (
                  f"안녕하세요. 저는 {personality.name}이에요. "
                  f"오늘은 어떤 이야기를 나눠볼까요?"
            )

            # 8. 대화 기억 저장
            memory_engine.save_memory(
                  user_message=message,
                  ai_response=reply
            )

            return {
                  "character_name": personality.name,
                  "reply": reply,
                  "emotion": emotion_data,
                  "relationship": relationship.model_dump(
                        mode="json"
                  ),
                  "memories": [
                        memory.model_dump(mode="json")
                        for memory in memories
                  ],
                  "recent_memories": [
                        memory.model_dump(mode="json")
                        for memory in recent_memories
                  ],
                  "personality_prompt": personality_prompt,
                  "mode": "demo"
            }

ai_orchestrator = AIOrchestrator()