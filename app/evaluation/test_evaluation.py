from app.scripts.conversation_rag import llm, conversational_rag, conversation_service, retrieval_service
from app.evaluation.generation_evaluator import GenerationEvaluator
from app.evaluation.dataset import EVALUATION_DATASET
from app.evaluation.ollama_llm_judge import OllamaLLMJudge
from app.evaluation.retrieval_evaluator import RetrievalEvaluator

judge=OllamaLLMJudge(llm=llm)

generation_evaluation=GenerationEvaluator(rag_service=conversational_rag,judge=judge)

session_id = conversation_service.create_session()

res=generation_evaluation.evaluate(EVALUATION_DATASET,session_id)

for i, item in enumerate(res, start=1):
    print(f"\n{'=' * 100}")
    print(f"Evaluation {i}")
    print(f"{'=' * 100}")

    print(f"Correctness  : {item['correctness']}")
    print(f"Faithfulness : {item['faithfulness']}")
    print(f"Relevance    : {item['relevance']}")
    print(f"Reason       : {item['reason']}")

print(f"\n{'=' * 100}")

retrieval_evaluation=RetrievalEvaluator(retrieval_service)

res2=retrieval_evaluation.evaluate(EVALUATION_DATASET)
print(f"\n{'=' * 100}")
print("retrieval evaluation metrix")
print(f"{'=' * 100}")
print(f"Recall  : {res2['recall_at_k']}")
print(f"Precision : {res2['precision_at_k']}")
print(f"MRR    : {res2['mrr']}")
