from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.vectordb.qdrant import Qdrant
from phi.knowledge.text import TextKnowledgeBase



from dotenv import load_dotenv

load_dotenv()


from phi.vectordb.pgvector import PgVector


# create vectordb
vector_db = Qdrant(
    collection="phidata-qdrant-liam-demo",
    url="http://localhost:6333",
)


knowledge_base_txt = TextKnowledgeBase(
    path="transcripts/",
    # Table name: ai.text_documents
    vector_db=vector_db
)

# Load the knowledge base: Comment after first run as the knowledge base is already loaded
knowledge_base_txt.load(upsert=True)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge_base_txt,
    search_knowledge=True,
    show_tool_calls=True,
    markdown=True,
    add_history_to_messages=True,
)



user = input("Enter your query here")

while True:
    if user == "exit":
        break
    else:
        sys_prompt = "if you do not know the answer just simply say I dont know"
        agent.print_response(user+sys_prompt , stream=True)
        user = input("Enter your query here :->>> ")
        
