# 기억 저장소
import json

from pathlib import Path
from threading import Lock

from app.memory.models import MemoryRecord

class MemoryStorage:
      def __init__(self):
            self.data_dir = Path(__file__).resolve().parents[2] / "data"
            self.file_path = self.data_dir / "memories.json"
            self.lock = Lock()

            self.data_dir.mkdir(parents=True, exist_ok=True)

            if not self.file_path.exists():
                  self.file_path.write_text(
                        "[]",
                        encoding="utf-8"
                  )

      def load(self):
            with self.lock:
                  try:
                        data = json.loads(
                              self.file_path.read_text(
                                    encoding="utf-8"
                              )
                        )

                        return [
                              MemoryRecord.model_validate(item)
                              for item in data
                        ]

                  except (json.JSONDecodeError, ValueError):
                        return []

      def save(self, memories: list[MemoryRecord]):
            with self.lock:
                  data = [
                        memory.model_dump(mode="json")
                        for memory in memories
                  ]

                  self.file_path.write_text(
                        json.dumps(
                              data,
                              ensure_ascii=False,
                              indent=2
                        ),
                        encoding="utf-8"
                  )

memory_storage = MemoryStorage()