import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

# Fast local model for interactive questions
MODEL_NAME = "qwen2.5:1.5b"


def ask_ollama(
    prompt: str,
    temperature: float = 0.1,
) -> str:

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()

        answer = result.get(
            "response",
            "",
        ).strip()

        if not answer:
            return "The AI returned an empty response."

        return answer

    except requests.exceptions.Timeout as exc:

        raise RuntimeError(
            "Ollama took too long to respond. "
            "The local model may still be loading."
        ) from exc

    except requests.exceptions.RequestException as exc:

        raise RuntimeError(
            f"Unable to connect to Ollama: {exc}"
        ) from exc
