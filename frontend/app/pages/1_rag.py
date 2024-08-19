import streamlit as st
from io import StringIO
from pages.common import load_sample_files

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pages.lib.pinecone import get_index, stream_to_file

SAMPLE_FILES_PATH = "app/sample_files"

@st.cache_data
def load_contents(files, path):
    file_content = []
    for f in files:
        with open(f"{path}/{f}", "rb") as file:
            file_content.append(file.read())
    return file_content


st.set_page_config(layout="wide")

## Access The Pinecone index
try:
    pc_index = get_index()
except Exception as e:
    st.write(f"Error accesing pinecone: {e}")
    st.stop()


col1, col2 = st.columns([1, 1])
with col1:
    st.write("## Sample Files, or pick your own")
    files, ext = load_sample_files(SAMPLE_FILES_PATH)
    file_content = load_contents(files, SAMPLE_FILES_PATH)
    ext_cols = st.columns(len(files))
    for i in range(len(files)):
        ext_cols[i].download_button(
            label=ext[i], 
            data=file_content[i], 
            file_name=files[i], 
            mime="application/octet-stream")
    
    st.write("## File Uploader")
    st.write("Upload a file PDF, Docx or txt to be processed.")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        
        file_path = stream_to_file(uploaded_file)
        st.write(file_path)
        

with col2:
    stats =pc_index.describe_index_stats()
    st.write("## Pinecone Index Stats")
    st.write(f"Index Name: **{pc_index.name}**")
    st.write(stats)

## RAG Chatbot
st.divider()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an AI knowledgebase answer question using only information from the context provided below.
        IF you cannot answer just say "I don't know"."""),
        ("system", "Context:\n{context}"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI()


# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    
    ## Search for context in the knowledge base
    
    config = {"configurable": {"session_id": "any"}}
    response = chain.invoke({"question": prompt, "context":""}, config)
    st.chat_message("ai").write(response.content)

