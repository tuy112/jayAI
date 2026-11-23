from app.emotion.models import EmotionState

class EmotionEngine:

      def __init__(self):
            self.state = EmotionState()

            self.emotion_keywords = {
                  "happiness": [
                        "좋아", "고마워", "행복", "최고", "잘했어"
                  ],
                  "sadness": [
                        "슬퍼", "힘들어", "우울", "외로워", "속상해"
                  ],
                  "anger": [
                        "화나", "짜증", "싫어", "분노", "열받아"
                  ],
                  "curiosity": [
                        "궁금", "알고 싶어", "어떻게", "왜", "무엇"
                  ],
                  "loneliness": [
                        "혼자", "외로워", "보고 싶어"
                  ],
                  "anxiety": [
                        "불안", "걱정", "무서워", "두려워"
                  ]
            }

      def update(self, text: str):
            text = text.lower()

            for emotion, keywords in self.emotion_keywords.items():
                  matched = any(
                        keyword in text
                        for keyword in keywords
                  )

                  if matched:
                        current = getattr(self.state, emotion)

                        setattr(
                              self.state,
                              emotion,
                              min(100, current + 15)
                        )

            return self.state

      def get_state(self):
            return self.state

      def reset(self):
            self.state = EmotionState()
            return self.state


emotion_engine = EmotionEngine()