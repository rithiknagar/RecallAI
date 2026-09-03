from app.evaluation.llm_judge import LLMJudge
from app.generation.ollama_llm import OllamaLLM
from app.evaluation.evaluation_prompt import JUDGE_PROMPT
import json


class OllamaLLMJudge(LLMJudge):

    def __init__(
        self,
        llm: OllamaLLM,
    ) -> None:

        self._llm = llm


    def _parse_response(
        self,
        response: str,
    ) -> dict:

        response = response.strip()

        if response.startswith("```"):
            response = response.split("\n", 1)[1]
            response = response.rsplit("```", 1)[0]
            response = response.strip()

        try:

            return json.loads(response)

        except json.JSONDecodeError as exc:

            raise ValueError(
                f"Judge returned invalid JSON: {response!r}"
            ) from exc

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str,
        reference_answer: str,
    ) -> dict:

        prompt = JUDGE_PROMPT.format(
            question=question,
            context=context,
            answer=answer,
            reference_answer=reference_answer,
        )

        response = self._llm.generate(prompt)
        
        # print(repr(response))

        return self._parse_response(response)