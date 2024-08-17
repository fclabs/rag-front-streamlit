import streamlit as st
import os
from utils.files import read_file_text

README_PATH = "app/README.md"


####################
# Streamlite setup #
st.markdown(read_file_text(README_PATH))

api_key = st.sidebar.text_input(
    "Enter your OpenAI API key", value="")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
with st.sidebar.expander("About this app"):
    st.write(
        """
        This app demonstrates how to use the LangChain library to create a chatbot with Streamlit.
        """
    )