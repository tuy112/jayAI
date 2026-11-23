from datetime import datetime, timezone
from threading import Lock

from app.relationship.models import (
      RelationshipState,
      RelationshipEvent
)
from app.relationship.storage import relationship_storage

class RelationshipEngine:
      def __init__(self):
            self.storage = relationship_storage
            self.lock = Lock()

            self.event_changes = {
                  RelationshipEvent.POSITIVE: {
                        "familiarity": 2,
                        "trust": 1,
                        "affection": 2,
                        "respect": 1
                  },
                  RelationshipEvent.SUPPORTIVE: {
                        "familiarity": 2,
                        "trust": 3,
                        "affection": 2,
                        "respect": 2
                  },
                  RelationshipEvent.PROMISE_KEPT: {
                        "familiarity": 1,
                        "trust": 5,
                        "affection": 1,
                        "respect": 3
                  },
                  RelationshipEvent.CONFLICT: {
                        "familiarity": 0,
                        "trust": -3,
                        "affection": -3,
                        "respect": -2
                  },
                  RelationshipEvent.APOLOGY: {
                        "familiarity": 0,
                        "trust": 2,
                        "affection": 2,
                        "respect": 2
                  },
                  RelationshipEvent.NEUTRAL: {
                        "familiarity": 1,
                        "trust": 0,
                        "affection": 0,
                        "respect": 0
                  }
            }

      def get_state(self):
            return self.storage.load()

      def update(self, event: RelationshipEvent):
            with self.lock:
                  state = self.storage.load()
                  changes = self.event_changes[event]

                  for field, change in changes.items():
                        current = getattr(state, field)

                        setattr(
                              state,
                              field,
                              max(0, min(100, current + change))
                        )

                  state.interaction_count += 1
                  state.updated_at = datetime.now(timezone.utc)

                  self.storage.save(state)

                  return state

      def reset(self):
            with self.lock:
                  state = RelationshipState()
                  self.storage.save(state)

                  return state

relationship_engine = RelationshipEngine()