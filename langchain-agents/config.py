import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=API_KEY,
    max_retries=2

)

employee = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=API_KEY,
    max_retries=2
)



