import os
import requests


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL_NAME = "openai/gpt-oss-20b"


def ask_groq(
    prompt: str,
    temperature: float = 0.1,
) -> str:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": temperature,
        "max_completion_tokens": 500,
        "reasoning_effort": "low",
        "include_reasoning": False,
    }

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        choices = result.get("choices", [])

        if not choices:
            return "The AI returned no answer."

        answer = (
            choices[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not answer:
            return "The AI returned an empty response."

        return answer

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Groq took too long to respond."
        ) from exc

    except requests.exceptions.RequestException as exc:

        try:
            error_detail = response.json().get(
                "error", {}
            ).get(
                "message",
                str(exc),
            )
        except Exception:
            error_detail = str(exc)

        raise RuntimeError(
            f"Unable to connect to Groq: {error_detail}"
        ) from exc
