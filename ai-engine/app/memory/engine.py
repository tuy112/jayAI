from uuid import uuid4

from app.memory.models import MemoryRecord
from app.memory.storage import memory_storage

class MemoryEngine:
      def __init__(self):
            self.storage = memory_storage

      def save_memory(
            self,
            user_message: str,
            ai_response: str
      ):
            memories = self.storage.load()
            memory = MemoryRecord(
                  memory_id=str(uuid4()),
                  user_message=user_message,
                  ai_response=ai_response
            )

            memories.append(memory)
            self.storage.save(memories)

            return memory

      def get_recent_memories(self, limit: int = 10):
            memories = self.storage.load()
            
            return memories[-limit:][::-1]

      def search_memories(self, keyword: str):
            memories = self.storage.load()
            keyword = keyword.strip().lower()

            if not keyword:
                  return []

            results = [
                  memory
                  for memory in memories
                  if keyword in memory.user_message.lower()
                  or keyword in memory.ai_response.lower()
            ]

            return results[::-1]

      def clear_memories(self):
            self.storage.save([])
            return True

memory_engine = MemoryEngine()