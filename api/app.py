from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os 
from dotenv import load_dotenv

load_dotenv()

# Set the OpenAI API key
api_key = os.getenv("OPEN_API_KEY")

# LangSmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

# Create the FastAPI app
app = FastAPI(
    title="LangChain Chatbot",
    description="A chatbot powered by LangChain",
    version="1.0"
)

# Add the routes for application  
add_routes(
    app, 
    ChatOpenAI(),
    path='/openai',
)

# Setting up the model
model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

# Prompt templates
prompt1 = ChatPromptTemplate.from_template("Write an essay about {topic}. It should be 100 words long.")
prompt2 = ChatPromptTemplate.from_template("Write an poem about {topic}. It should be 100 words long.")

# Add the routes for essays
add_routes(
    app,
    # model,
    prompt1|model,
    path="/essay"
)

# Add the routes for poems
add_routes(
    app,
    # model,
    prompt2|model,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)