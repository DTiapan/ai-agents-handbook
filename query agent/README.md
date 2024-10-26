# Custom AI Agent with Python

🚀 **Building Your Custom AI Agent with Python: A Step-by-Step Guide!** 🚀

In today’s fast-paced, AI-driven landscape, businesses are increasingly seeking tailored AI agents to optimize their workflows. This repository contains a concise guide to help you create your own AI agent using Python!

## Table of Contents

- [Overview](#overview)
- [Framework of Choice: LangChain](#framework-of-choice-langchain)
- [Getting Started](#getting-started)
- [Code Snippet](#code-snippet)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project aims to set up a basic AI agent capable of answering questions based on various documents (PDFs, web pages, etc.). Using the LangChain framework, we can build an intelligent agent that communicates and reasons effectively.

## Framework of Choice: LangChain

LangChain is our framework of choice, designed to streamline the development of AI-powered applications. It efficiently manages data, integrations, and conversational logic, making it perfect for building intelligent agents.

## Getting Started

### Prerequisites

- Python 3.x
- A valid OpenAI API key
- Install required packages

```bash
pip install langchain python-dotenv faiss-cpu
```

### Environment Variables

Create a `.env` file in the root of your project and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Code Snippet

Here’s a quick code snippet to get you started:

```python
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
loader = LocalFileLoader("path/to/your/documents/")
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
```

## How It Works

1. **Initialization**: Set up the LLM model (OpenAI) and FAISS for document indexing.
2. **Document Loading**: Import relevant files into the agent's memory for information retrieval.
3. **Agent Execution**: When a question is posed, the agent finds relevant content and generates an answer.

## Customization

Take it a step further! Customize your agent by integrating complex workflows, adding memory capabilities, or connecting to APIs for dynamic, real-time responses.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

🔄 **Ready to enhance your productivity with AI? Follow me for more insightful tutorials and tips!**

#AI #MachineLearning #Python #AIAgent #LangChain #OpenAI #PythonAI
