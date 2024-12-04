import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from typing_extensions import Annotated
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()

# Set the OpenAI API key
openai_api_key = os.getenv("OPEN_API_KEY")

# Check if the API key is loaded
if openai_api_key:
    print("API Key loaded successfully:", openai_api_key)
else:
    print("Failed to load API Key.")
    st.error("API key is not set. Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define the state
class State(TypedDict):
    messages: Annotated[list, "The messages in the conversation"]

# Create a Streamlit callback handler
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# Set up the LLM
llm = ChatOpenAI(temperature=0, streaming=True, openai_api_key=openai_api_key)

# Create the graph
graph = StateGraph(State)

# Define the chatbot node
def chatbot(state: State):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

# Set up the graph
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

# Compile the graph
app = graph.compile()

# Streamlit UI
st.title("LangChain + LangGraph + Streamlit Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream_container = st.empty()
        with stream_container:
            callback = StreamlitCallbackHandler(stream_container)
            response = app.invoke(
                {"messages": st.session_state.messages},
                {"callbacks": [callback]}
            )
        assistant_message = response["messages"][-1]
        st.session_state.messages.append({"role": "assistant", "content": assistant_message.content})