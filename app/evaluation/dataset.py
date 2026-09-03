from app.evaluation.models import EvaluationSample


EVALUATION_DATASET = [

    EvaluationSample(
        question="How many Monthly leave days do employees receive?",
        relevant_chunk_ids={22, 23},
        expected_answer="You are entitled to one sick or casual leave per month"
    ),

    EvaluationSample(
        question="What is Notice period ?",
        relevant_chunk_ids={11,78,79},
        expected_answer="For employees on probation, the notice period is 30 days, while for full-time employees, the notice period is 60 days."
    ),

    EvaluationSample(
        question="How far in advance are employees required to submit leave requests?",
        relevant_chunk_ids={22},
        expected_answer="Employees are required to submit leave requests at least one week in advance."
    ),
]