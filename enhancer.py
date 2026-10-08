import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert prompt engineer for text-to-image diffusion models.

Given a short idea and a style, return ONLY a JSON object with these keys:

- "prompt": a detailed, vivid image prompt covering subject, setting, lighting,
  composition, mood, camera/medium details. Maximum 80 words.
- "negative_prompt": comma-separated things to avoid
  (e.g. blurry, distorted hands, low quality, watermark)
- "style": a short label for the style you applied

Do not add any text outside the JSON."""


def enhance_prompt(idea: str, style: str = "None") -> dict:
    user_msg = f"Idea: {idea}\nStyle: {style}"

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    return json.loads(response.choices[0].message.content)