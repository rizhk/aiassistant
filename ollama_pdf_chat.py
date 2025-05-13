from agno.agent import Agent
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.ollama import Ollama
from agno.vectordb.pgvector import PgVector
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# 🔧 Define db_url first
db_url = "postgresql+psycopg://rizwanmushtaq:ai_pass@localhost:5432/ai"

def is_knowledge_empty(kb):
    engine = create_engine(db_url)
    table_name = kb.vector_db.table_name

    # 🔍 First check if table exists
    with engine.connect() as conn:
        # 💡 Query to check if table exists
        result = conn.execute(text(
            f"SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = '{table_name}')"
        ))
        table_exists = result.scalar()

        if not table_exists:
            return True  # Table doesn't exist → treat as empty

        # Now check if it has data
        try:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            return count == 0
        except ProgrammingError:
            return True  # Handle any other SQL errors gracefully

# 📄 Initialize knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://wedigitify.com/wp-content/uploads/2024/07/AnOverviewOfTransformingYourBusinesswithAIAgents.pdf"],
    vector_db=PgVector(
        table_name="ai_pdf_knowledge_base",
        db_url=db_url,
        embedder=OllamaEmbedder(id="gemma:2b", dimensions=2048),
    ),
)

# 🚀 Load only if empty
if is_knowledge_empty(knowledge_base):
    print("🧠 Knowledge base is empty or missing. Loading...")
    knowledge_base.load(recreate=True)
else:
    print("📚 Knowledge already exists. Skipping load.")

# 🤖 Create agent
agent = Agent(
    model=Ollama(id="gemma:2b"),
    knowledge=knowledge_base,
    show_tool_calls=True,
)

# 🧪 Optional: Run a test query
message = agent.run("What is the name inside the pdf?", markdown=True)
print(message)