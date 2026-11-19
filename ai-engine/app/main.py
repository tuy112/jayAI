from fastapi import FastAPI

from app.personality.profile import (
      get_personality,
      get_personality_prompt
)

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