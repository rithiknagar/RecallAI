from app.conversation.ollama_query_rewriter import (
    OllamaQueryRewriter,
)

from app.conversation.rag_query_rewrite_prompt import (
    RAGQueryRewritePromptBuilder,
)

from app.conversation.postgres_repository import (
    PostgresConversationRepository,
)

from app.conversation.service import (
    ConversationService,
)

from app.generation.ollama_llm import OllamaLLM

from app.core.database import SessionLocal

session = SessionLocal()

repository = PostgresConversationRepository(
    session
)

conversation_service = ConversationService(
    repository
)

llm = OllamaLLM(
    model="gemma3",
    base_url="http://localhost:11434",
)

prompt_builder = (
    RAGQueryRewritePromptBuilder()
)

query_rewriter = OllamaQueryRewriter(
    llm=llm,
    prompt_builder=prompt_builder,
)

session_id = (
    conversation_service
    .create_session()
)

conversation_service.add_message(
    session_id=session_id,
    role="user",
    content="How many annual leave days do employees get?",
)

conversation_service.add_message(
    session_id=session_id,
    role="assistant",
    content="Employees receive 27 days of annual leave.",
)

history = (
    conversation_service
    .get_history(session_id)
)

question = "What is the employee termination policy?"

rewritten = query_rewriter.rewrite(
    question=question,
    history=history,
)

print("Original:")
print(question)

print("\nRewritten:")
print(rewritten)