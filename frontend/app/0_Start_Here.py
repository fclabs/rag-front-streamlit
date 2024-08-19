import streamlit as st
import os
from utils.files import read_file_text

README_PATH = "app/README.md"


####################
# Streamlite setup #
st.markdown(read_file_text(README_PATH))



api_key = st.sidebar.text_input(
    "Enter your OpenAI API key", value=os.environ.get("OPENAI_API_KEY",""))
pinecone_api_key = st.sidebar.text_input(
    "Enter your Pinecone API key", value=os.environ.get("PINECONE_API_KEY",""))

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
if pinecone_api_key:
    os.environ["PINECONE_API_KEY"] = pinecone_api_key
    
with st.sidebar.expander("About this app"):
    st.write(
        """
        This app demonstrates how to use the LangChain library to create a chatbot with Streamlit.
        """
    )