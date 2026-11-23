from app.autonomy.models import (
      AutonomyRequest,
      AutonomyResponse,
      AutonomousAction
)

class AutonomyEngine:
      def decide(self, request: AutonomyRequest):
            minutes = request.minutes_since_interaction
            energy = request.energy

            # 에너지가 부족하면 휴식 우선
            if energy <= 20:
                  return AutonomyResponse(
                        action=AutonomousAction.REST,
                        message="조금 쉬어야겠어요.",
                        reason="에너지가 부족합니다."
                  )

            # 오랫동안 대화가 없으면 혼잣말
            if minutes >= 60 and request.allow_self_talk:
                  return AutonomyResponse(
                        action=AutonomousAction.SELF_TALK,
                        message="오늘은 무슨 이야기를 나눠볼까요?",
                        reason="사용자와 오랫동안 대화하지 않았습니다."
                  )

            # 일정 시간 대화가 없으면 주변 둘러보기
            if minutes >= 15:
                  return AutonomyResponse(
                        action=AutonomousAction.LOOK_AROUND,
                        message="주변을 둘러보고 있어요.",
                        reason="일정 시간 대화가 없었습니다."
                  )

            # 짧은 시간 대화가 없으면 생각하기
            if minutes >= 5:
                  return AutonomyResponse(
                        action=AutonomousAction.THINK,
                        message="잠시 생각하고 있어요.",
                        reason="잠시 대화가 중단되었습니다."
                  )

            # 기본 대기
            return AutonomyResponse(
                  action=AutonomousAction.IDLE,
                  message="기다리고 있어요.",
                  reason="현재 특별한 행동이 필요하지 않습니다."
            )

autonomy_engine = AutonomyEngine()