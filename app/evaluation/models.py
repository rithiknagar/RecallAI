from dataclasses import dataclass


@dataclass
class EvaluationSample:

    question: str
    relevant_chunk_ids: set[int]
    expected_answer:str