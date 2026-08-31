import requests

from app.generation.llm import LLM


class OllamaLLM(LLM):

    def __init__(
        self,
        model: str,
        base_url: str,
    ):
        self._model = model
        self._base_url = base_url

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = requests.post(
            f"{self._base_url}/api/generate",
            json={
                "model": self._model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]