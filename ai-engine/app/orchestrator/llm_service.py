import os
import json
import asyncio
import urllib.request
import urllib.error

from dotenv import load_dotenv

load_dotenv()

async def generate_reply(
      personality_prompt: str,
      emotion: dict,
      relationship: dict,
      memories: list,
      user_message: str
) -> str:
      base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
      )
      model_name = os.getenv(
            "OLLAMA_MODEL",
            "qwen3:4b"
      )
      prompt = f"""

[캐릭터 성격]
{personality_prompt}

[현재 감정 상태]
{emotion}

[사용자와의 관계]
{relationship}

[과거 기억]
{memories}

[대화 원칙]
- 자신의 성격을 일관되게 유지하세요.
- 현재 감정 상태를 대화에 자연스럽게 반영하세요.
- 과거 기억을 적절하게 활용하세요.
- 기억에 없는 사실을 기억한다고 주장하지 마세요.
- 감정을 과장하거나 매번 설명하지 마세요.
- 자연스러운 한국어 존댓말로 대화하세요.

[사용자 메시지]
{user_message}
"""

      request_data = json.dumps({
            "model": model_name,
            "messages": [
                  {
                        "role": "user",
                        "content": prompt
                  }
            ],
            "stream": False
      }).encode("utf-8")

      def call_ollama():
            request = urllib.request.Request(
                  url=f"{base_url}/api/chat",
                  data=request_data,
                  headers={
                        "Content-Type": "application/json"
                  },
                  method="POST"
            )

            with urllib.request.urlopen(
                  request,
                  timeout=120
            ) as response:

                  return json.loads(
                        response.read().decode("utf-8")
                  )

      try:
            result = await asyncio.to_thread(
                  call_ollama
            )

            reply = result.get(
                  "message", {}
            ).get("content", "")

            if not reply:
                  raise RuntimeError(
                        "로컬 AI 모델에서 응답을 반환하지 않았습니다."
                  )
            
            print("로컬 AI 응답 수신 완료", flush=True)

            return reply

      except urllib.error.URLError as error:
            raise RuntimeError(
                  f"Ollama 서버 연결 실패: {error}"
            ) from error