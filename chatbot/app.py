import getpass
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
import streamlit as st
# can you import StrOutputParser from langchain
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Set the OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv("OPEN_API_KEY")

# LangSmith Tracking 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

prompt = ChatPromptTemplate(
    [
        ("system", 'You are helpful assistant'),
        # ("user", "I need a lot of help with understanding controversial topics in our tradition."),
    ]
)


# Streamlit framework

st.title("LangChain Chatbot")
input_text = st.text_input("Enter your message")
# Initialize your parser
output_parser = StrOutputParser()

model = ChatOpenAI(model="gpt-3.5-turbo")
output = model.invoke([HumanMessage(content=input_text)])

chain = prompt|model|output_parser

st.write("""
    Ask a question to the chatbot and it will respond.
""")

if st.button("Send"):
    if input_text:
        # response = model.invoke([HumanMessage(content=input_text)])
        st.write(chain.invoke({'question': input_text}))
