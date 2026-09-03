JUDGE_PROMPT = """
You are evaluating the quality of a RAG system.

Evaluate the generated answer using the question,
reference answer, and retrieved context.

Question:
{question}

Reference answer:
{reference_answer}

Retrieved context:
{context}

Generated answer:
{answer}

Evaluate the following:

1. Correctness:
Does the generated answer correctly answer the question
and agree with the reference answer?

2. Faithfulness:
Are the claims in the generated answer supported by the
retrieved context?

3. Relevance:
Does the answer directly answer the question without
unnecessary information?

Give each score from 0 to 1.

Return ONLY valid JSON:

{{
    "correctness": 0.0,
    "faithfulness": 0.0,
    "relevance": 0.0,
    "reason": "brief explanation"
}}
"""