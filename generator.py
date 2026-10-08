import os
from io import BytesIO
from urllib.parse import quote

import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

MODEL = "flux"

API_URL = "https://gen.pollinations.ai/image"


def generate_image(
    prompt,
    negative_prompt="",
    width=1024,
    height=1024,
    seed=None
):
    api_key = os.getenv("POLLINATIONS_API_KEY")

    if not api_key:
        raise RuntimeError(
            "POLLINATIONS_API_KEY is missing from your .env file."
        )

    if seed is None:
        seed = -1

    encoded_prompt = quote(prompt, safe="")

    params = {
        "model": MODEL,
        "width": width,
        "height": height,
        "seed": seed,
        "nologo": "true",
        "private": "true",
    }

    if negative_prompt:
        params["negative_prompt"] = negative_prompt

    url = f"{API_URL}/{encoded_prompt}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=180
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Pollinations API error {response.status_code}: "
            f"{response.text[:500]}"
        )

    try:
        return Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        raise RuntimeError(
            f"Pollinations returned an invalid image: {e}"
        )