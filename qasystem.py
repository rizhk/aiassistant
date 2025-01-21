from langchain.chains import load_qa_chain
from langchain import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Initialize LLM
llm = OpenAI(model="text-davinci-003", temperature=0)

# Load Q&A Chain
qa_chain = load_qa_chain(llm)

# Ask a question
question = "What is LangChain?"
response = qa_chain.run({"input_documents": [], "question": question})
print(response)
