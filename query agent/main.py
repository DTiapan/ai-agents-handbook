from dotenv import load_dotenv
import os
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import LocalFileLoader

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI Model
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up a document loader for text files or PDFs
loader = LocalFileLoader("https://example-files.online-convert.com/document/txt/example.txt")
documents = loader.load()

# Use FAISS to index document embeddings
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
doc_search = FAISS.from_documents(documents, embeddings)

# Define Prompt Template
template = "Given the following document text, answer the question: {question}"
prompt = PromptTemplate(input_variables=["question"], template=template)
chain = LLMChain(prompt=prompt, llm=llm)

# Function to generate response
def query_agent(question):
    results = doc_search.similarity_search(question)
    if results:
        answer = chain.run(question=question, document=results[0].page_content)
        return answer
    return "No relevant information found."

# Test the Agent
response = query_agent("What is the main benefit of using AI in business?")
print("Agent Response:", response)
