# Creating web app, a front end to interact with the api 
import requests
import streamlit as st

# Function to get response from the essay model
def get_response_essay(input_text):
    response = requests.post(
        "http://localhost:8000/essay/invoke", 
        json = {
            "input": {'topic': input_text}
        }
    )

    return response.json()['output']['content']

# Function to get response from the poem model
def get_response_poem(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke", 
        json = {
            "input": {'topic': input_text}
        }
    )

    return response.json()['output']['content']

# Title
st.title("LangChain Chatbot")

# Input
input_text_essay = st.text_input("Enter your topic for essay")
input_text_poem = st.text_input("Enter your topic for poem")

# Button
if st.button("Send"):
    if input_text_essay:
        response = get_response_essay(input_text_essay)
        st.write(response)
    if input_text_poem:
        response = get_response_poem(input_text_poem)
        st.write(response)