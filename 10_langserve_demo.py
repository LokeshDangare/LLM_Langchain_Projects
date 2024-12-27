import os
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

_ = load_dotenv(find_dotenv())
groq_api_key = os.environ["GROQ_API_KEY"]

llm = ChatGroq(model="llama3-70b-8192")

output_parser = StrOutputParser()

system_template = "Translate the following into {language}: "

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

chain = prompt_template | llm | output_parser

app = FastAPI(
    title= "Simple Translator",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces",
)

add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)