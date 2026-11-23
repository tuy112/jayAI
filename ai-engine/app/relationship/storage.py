import json

from pathlib import Path
from threading import Lock

from app.relationship.models import RelationshipState

class RelationshipStorage:
      def __init__(self):
            self.data_dir = Path(__file__).resolve().parents[2] / "data"
            self.file_path = self.data_dir / "relationship.json"
            self.lock = Lock()

            self.data_dir.mkdir(parents=True, exist_ok=True)

            if not self.file_path.exists():
                  self.save(RelationshipState())

      def load(self):
            with self.lock:
                  try:
                        data = json.loads(
                              self.file_path.read_text(encoding="utf-8")
                        )

                        return RelationshipState.model_validate(data)

                  except (json.JSONDecodeError, ValueError):
                        return RelationshipState()

      def save(self, state: RelationshipState):
            with self.lock:
                  self.file_path.write_text(
                        state.model_dump_json(indent=2),
                        encoding="utf-8"
                  )

relationship_storage = RelationshipStorage()